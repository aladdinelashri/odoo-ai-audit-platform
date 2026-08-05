"""Audit log router using API_KEY dependency."""
import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from database.core.storage.base_pool import DatabasePool
from api.deps import get_db_pool
import structlog

logger = structlog.get_logger()
router = APIRouter(prefix="/audits", tags=["audits"])

API_KEY = os.getenv("API_KEY", "audit-log-api-key-change-me")


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key header."""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True


@router.get("/")
def list_audit_logs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db_pool: DatabasePool = Depends(get_db_pool),
    authorized: bool = Depends(verify_api_key),
):
    """List audit logs (requires X-API-KEY header, NOT JWT)."""
    # Audit events are emitted via structured logging
    return {
        "message": "Audit logs are emitted via structured logging. Query your log aggregator.",
        "skip": skip,
        "limit": limit,
    }
