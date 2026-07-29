# reports.py
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from database.core.reporting.service import ReportService
from database.core.reporting.ast import QueryAST

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])

# ---------- Pydantic models ----------
class ReportCreate(BaseModel):
    name: str
    description: Optional[str] = None
    query_ast: Dict[str, Any]
    parameters: Optional[List[Dict]] = None
    schedule: Optional[str] = None
    export_format: Optional[str] = "json"
    recipients: Optional[List[str]] = None

class ReportUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    query_ast: Optional[Dict[str, Any]] = None
    parameters: Optional[List[Dict]] = None
    schedule: Optional[str] = None
    export_format: Optional[str] = None
    recipients: Optional[List[str]] = None
    status: Optional[str] = None

class ReportResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    query_ast: Dict[str, Any]
    parameters: List[Dict]
    schedule: Optional[str]
    export_format: str
    recipients: List[str]
    created_at: str
    updated_at: Optional[str]
    last_run: Optional[str]
    next_run: Optional[str]
    status: str

# ---------- Endpoints ----------
@router.post("/", response_model=ReportResponse)
def create_report(report: ReportCreate):
    report_id = ReportService.create_report(
        name=report.name,
        query_ast=report.query_ast,
        description=report.description,
        parameters=report.parameters,
        schedule=report.schedule,
        export_format=report.export_format,
        recipients=report.recipients,
    )
    return ReportService.get_report(report_id)

@router.get("/", response_model=List[ReportResponse])
def list_reports(status: Optional[str] = Query(None)):
    return ReportService.list_reports(status)

@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int):
    report = ReportService.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.put("/{report_id}", response_model=ReportResponse)
def update_report(report_id: int, report_update: ReportUpdate):
    # Convert to dict, remove None values
    update_data = {k: v for k, v in report_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    success = ReportService.update_report(report_id, **update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportService.get_report(report_id)

@router.delete("/{report_id}")
def delete_report(report_id: int):
    success = ReportService.delete_report(report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"detail": "Report deleted"}

@router.post("/{report_id}/execute")
def execute_report(report_id: int, parameters: Optional[Dict[str, Any]] = None):
    try:
        result = ReportService.execute_report(report_id, parameters)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Execution failed: {str(e)}")
