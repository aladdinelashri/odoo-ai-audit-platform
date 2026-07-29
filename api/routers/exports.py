# exports.py
from fastapi import APIRouter

router = APIRouter(prefix="/exports", tags=["exports"])

@router.post("/pdf")
async def export_pdf():
    return {"message": "PDF export stub"}
