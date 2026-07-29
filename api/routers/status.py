# status.py
from fastapi import APIRouter

router = APIRouter(prefix="/status", tags=["status"])

@router.get("/")
async def system_status():
    return {"status": "ok", "components": {"sqlite": "connected"}}
