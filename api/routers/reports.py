import json
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query, Response
from pydantic import BaseModel

from api.auth import get_current_user, get_current_active_user, User
from api.deps import get_db_pool, limiter
from database.core.storage.base_pool import DatabasePool
from database.core.reporting.service import (
    create_report, get_report, list_reports, update_report, delete_report, execute_report
)
from database.core.reporting.audit import log_audit

# ---- Export support ----
from database.core.reporting.ast import validate_ast
from database.core.reporting.builder import SQLBuilder
from database.core.reporting.exports import export_json, export_excel, export_pdf
from database.core.storage.sqlite.sqlite_pool import get_sqlite_pool

router = APIRouter(prefix="/reports", tags=["reports"])

# ---------- Models ----------
class ReportCreate(BaseModel):
    name: str
    description: Optional[str] = None
    query_ast: dict
    parameters: Optional[dict] = {}
    schedule: Optional[Any] = None  # FIXED: accepts dict or string
    export_format: str = "json"
    recipients: List[str] = []

class ReportUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    query_ast: Optional[dict] = None
    parameters: Optional[dict] = None
    schedule: Optional[Any] = None  # FIXED: accepts dict or string
    export_format: Optional[str] = None
    recipients: Optional[List[str]] = None
    status: Optional[str] = None

class ReportOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    query_ast: dict
    parameters: dict
    schedule: Optional[Any]  # FIXED
    export_format: str
    recipients: List[str]
    status: str
    created_by: int
    created_at: str
    updated_at: Optional[str]
    last_run: Optional[str]
    next_run: Optional[str]

# ---------- Endpoints ----------
@router.post("/", response_model=ReportOut, status_code=201)
async def create_report_endpoint(
    report: ReportCreate,
    current_user: User = Depends(get_current_user),
    db_pool: DatabasePool = Depends(get_db_pool),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create reports")
    result = create_report(report.dict(), current_user.id, db_pool)
    return result

@router.get("/", response_model=List[ReportOut])
async def list_reports_endpoint(
    db_pool: DatabasePool = Depends(get_db_pool),
    current_user: User = Depends(get_current_active_user),
):
    return list_reports(db_pool)

@router.get("/{report_id}", response_model=ReportOut)
async def get_report_endpoint(
    report_id: int,
    db_pool: DatabasePool = Depends(get_db_pool),
    current_user: User = Depends(get_current_active_user),
):
    report = get_report(report_id, db_pool)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.put("/{report_id}", response_model=ReportOut)
async def update_report_endpoint(
    report_id: int,
    update: ReportUpdate,
    current_user: User = Depends(get_current_user),
    db_pool: DatabasePool = Depends(get_db_pool),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update reports")
    result = update_report(report_id, update.dict(exclude_unset=True), current_user.id, db_pool)
    if not result:
        raise HTTPException(status_code=404, detail="Report not found")
    return result

@router.delete("/{report_id}", status_code=204)
async def delete_report_endpoint(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db_pool: DatabasePool = Depends(get_db_pool),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete reports")
    success = delete_report(report_id, current_user.id, db_pool)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return None

@router.post("/{report_id}/trigger")
@limiter.limit("10/minute")
async def trigger_report_endpoint(
    request: Request,
    report_id: int,
    parameters: Optional[dict] = None,
    current_user: User = Depends(get_current_active_user),
    db_pool: DatabasePool = Depends(get_db_pool),
):
    try:
        result = execute_report(report_id, db_pool, parameters)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")

# ---------- EXPORT ----------
@router.get("/{report_id}/export")
async def export_report_endpoint(
    report_id: int,
    format: str = Query("json", enum=["json", "excel", "pdf"]),
    current_user: User = Depends(get_current_active_user),
    db_pool: DatabasePool = Depends(get_db_pool),
):
    """Export report data in JSON, Excel (XLSX), or PDF format."""
    report = get_report(report_id, db_pool)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    query_ast = report.get("query_ast")
    if isinstance(query_ast, str):
        query_ast = json.loads(query_ast)

    validate_ast(query_ast)
    sql, params = SQLBuilder.ast_to_sql(query_ast)

    sqlite_pool = get_sqlite_pool()
    with sqlite_pool.get_connection() as conn:
        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()

    report_name = report.get("name", "report")
    if format == "json":
        content_str = export_json(rows)
        content = content_str.encode("utf-8")
        media_type = "application/json"
        filename = f"{report_name}.json"
    elif format == "excel":
        content = export_excel(rows, sheet_name=report_name)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"{report_name}.xlsx"
    elif format == "pdf":
        content = export_pdf(rows, title=report_name)
        media_type = "application/pdf"
        filename = f"{report_name}.pdf"
    else:
        raise HTTPException(status_code=400, detail="Invalid format")

    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(content=content, media_type=media_type, headers=headers)
