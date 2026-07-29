# hermes.py
from fastapi import APIRouter

router = APIRouter(prefix="/hermes", tags=["hermes"])

@router.post("/query")
async def hermes_query():
    return {"message": "Hermes stub - will handle NLP"}
