import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import structlog
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from prometheus_client import make_asgi_app

# Import routers
from fastapi import status as http_status
from api.auth import router as auth_router, create_users_table
from api.routers import audits, hermes, status, export_async, reports  # <-- ADD THIS LINE

# Import scheduler and database
from database.core.reporting.scheduler import initialize_scheduler, shutdown_scheduler, get_scheduler
from database.core.storage.pool_factory import create_pool
from database.core.storage.base_pool import DatabasePool

# Import shared dependencies (to avoid circular import)
from api.deps import limiter, get_db_pool

# Import metrics (centralized)
from api.metrics import REPORT_EXECUTIONS, REPORT_DURATION, ACTIVE_JOBS  # noqa: F401

load_dotenv()

# ---------- Sentry ----------
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[StarletteIntegration(), FastApiIntegration()],
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
        environment=os.getenv("ENV", "production"),
    )

# ---------- Structured logging ----------
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
logger = structlog.get_logger()

# ---------- Configuration ----------
API_KEY = os.environ.get("API_KEY", "your-secure-api-key")
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=True)

async def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )
    return api_key

# ---------- FastAPI app ----------
app = FastAPI(
    title="Odoo AI Audit Platform API",
    description="Comprehensive audit, reporting, and AI integration",
    version="5.0",
)

# Mount Prometheus metrics app before any middleware
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Include routers ----------
app.include_router(audits.router, dependencies=[Depends(verify_api_key)])
app.include_router(hermes.router, dependencies=[Depends(verify_api_key)])
app.include_router(status.router, dependencies=[Depends(verify_api_key)])
app.include_router(export_async.router, dependencies=[Depends(verify_api_key)])
app.include_router(reports.router)  # JWT auth handled inside
app.include_router(auth_router)

# ---------- Enhanced health check ----------
@app.get("/health")
async def health_check(db_pool: DatabasePool = Depends(get_db_pool)):
    health_status = {
        "status": "healthy",
        "database": "ok",
        "scheduler": "ok",
        "version": "5.0"
    }
    # Check database
    try:
        db_pool.fetch_one("SELECT 1")
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        health_status["database"] = "error"
        health_status["status"] = "unhealthy"

    # Check scheduler using get_scheduler()
    try:
        sched = get_scheduler()
        if not sched.running:
            health_status["scheduler"] = "stopped"
            health_status["status"] = "unhealthy"
    except Exception as e:
        logger.error("Scheduler health check failed", error=str(e))
        health_status["scheduler"] = "error"
        health_status["status"] = "unhealthy"

    return health_status

# ---------- Lifespan events ----------
@app.on_event("startup")
async def startup_event():
    logger.info("Starting application...")
    db_pool = create_pool()
    app.state.db_pool = db_pool
    logger.info(f"Database pool initialized (type: {os.getenv('DATABASE_TYPE', 'sqlite')})")

    db_type = os.getenv("DATABASE_TYPE", "sqlite").lower()
    if db_type == "sqlite":
        create_users_table(db_pool)
    else:
        logger.info("PostgreSQL tables assumed created by Alembic.")
        create_users_table(db_pool)  # safe to call; it checks existence

    # Initialize scheduler with the database pool
    try:
        initialize_scheduler(db_pool)  # <-- Fixed: pass the pool
        logger.info("Scheduler started")
    except Exception as e:
        logger.error("Failed to start scheduler", error=str(e))

    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")
    try:
        shutdown_scheduler()
        logger.info("Scheduler shut down")
    except Exception as e:
        logger.error("Error during scheduler shutdown", error=str(e))
    try:
        app.state.db_pool.close()
        logger.info("Database pool closed")
    except Exception as e:
        logger.error("Error closing database pool", error=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=os.environ.get("API_HOST", "0.0.0.0"),
        port=int(os.environ.get("API_PORT", 8000)),
        reload=True,
    )
