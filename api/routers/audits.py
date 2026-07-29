# audits.py
from fastapi import APIRouter

router = APIRouter(prefix="/audits", tags=["audits"])

@router.get("/")
async def list_audits():
    return {"message": "Audits router - stub"}
