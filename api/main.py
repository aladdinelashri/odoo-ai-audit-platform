# api/main.py
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import all routers
from api.routers import audits, hermes, status, exports, reports

# Load environment variables
load_dotenv()

# ---------- Configuration ----------
API_KEY = os.environ.get("API_KEY", "your-secure-api-key")
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=True)

# ---------- Authentication dependency ----------
async def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )
    return api_key

# ---------- FastAPI app ----------
app = FastAPI(
    title="Odoo AI Audit Platform API",
    description="Comprehensive audit, reporting, and AI integration",
    version="5.0",
)

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Include routers with authentication ----------
# All routes under /api/v1 require API key
api_router = FastAPI()
api_router.include_router(audits.router, dependencies=[Depends(verify_api_key)])
api_router.include_router(hermes.router, dependencies=[Depends(verify_api_key)])
api_router.include_router(status.router, dependencies=[Depends(verify_api_key)])
api_router.include_router(exports.router, dependencies=[Depends(verify_api_key)])
api_router.include_router(reports.router, dependencies=[Depends(verify_api_key)])

app.mount("/api/v1", api_router)

# ---------- Public endpoint (no auth) ----------
@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "5.0"}

# ---------- Lifespan events ----------
@app.on_event("startup")
async def startup_event():
    """Initialise database connection pool on startup."""
    from database.core.storage.sqlite.sqlite_pool import SQLitePool
    import os

    db_path = os.environ.get("AUDIT_DB_PATH", "database/storage/audit.db")
    SQLitePool.initialize(db_path)
    print(f"SQLite pool initialized with WAL mode at {db_path}")

@app.on_event("shutdown")
async def shutdown_event():
    """Close all connections on shutdown."""
    from database.core.storage.sqlite.sqlite_pool import SQLitePool
    SQLitePool.close_all()
    print("SQLite pool closed")

# ---------- If running directly ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=os.environ.get("API_HOST", "0.0.0.0"),
        port=int(os.environ.get("API_PORT", 8000)),
        reload=True,
    )
