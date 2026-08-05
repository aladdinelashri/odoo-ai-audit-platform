"""Health and metrics router."""
from fastapi import APIRouter
from sqlalchemy import text
from api.core.database import engine, sqlite_engine
from api.services.report_service import _serialize_datetime_fields

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    """Basic health check."""
    return {"status": "healthy"}


@router.get("/health/db")
async def health_db():
    """Database health check."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        pg_status = "connected"
    except Exception as e:
        pg_status = f"error: {str(e)}"
    
    try:
        with sqlite_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        sqlite_status = "connected"
    except Exception as e:
        sqlite_status = f"error: {str(e)}"
    
    return _serialize_datetime_fields({
        "status": "healthy" if pg_status == "connected" and sqlite_status == "connected" else "degraded",
        "postgresql": pg_status,
        "sqlite": sqlite_status
    })


@router.get("/metrics")
async def metrics():
    """Basic metrics endpoint."""
    return {
        "uptime_seconds": 0,  # Would track actual uptime in production
        "requests_total": 0,
        "requests_per_second": 0.0
    }
