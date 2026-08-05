import asyncio
import json
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, Request, status
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from pydantic import BaseModel

from api.auth import get_current_active_user, User
from api.deps import get_db_pool, limiter
from database.core.storage.base_pool import DatabasePool
from database.core.reporting.service import ReportService
from database.core.reporting.exports import export_json, export_excel, export_pdf

router = APIRouter(prefix="/export", tags=["export"])

# ---------- Models ----------
class ExportRequest(BaseModel):
    report_id: int
    parameters: Optional[Dict[str, Any]] = None
    format: str = "excel"

class ExportResponse(BaseModel):
    task_id: str
    status: str
    message: str

# ---------- Background export (async) ----------
# We'll store tasks in memory (for demo); in production use Celery/Redis.
_tasks: Dict[str, Dict] = {}

@router.post("/async", response_model=ExportResponse)
@limiter.limit("5/minute")  # rate limit for export requests
async def create_export_task(
    request: Request,
    export_req: ExportRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db_pool: DatabasePool = Depends(get_db_pool),
):
    """
    Start an asynchronous export of a report.
    Returns a task ID to poll for status/download.
    """
    import uuid
    task_id = str(uuid.uuid4())
    _tasks[task_id] = {"status": "pending", "result": None, "error": None}

    # Run the export in background
    background_tasks.add_task(
        _run_export,
        task_id,
        export_req.report_id,
        export_req.parameters,
        export_req.format,
        current_user.id,
        db_pool,
    )
    return ExportResponse(task_id=task_id, status="pending", message="Export started")

async def _run_export(
    task_id: str,
    report_id: int,
    parameters: Optional[Dict],
    format: str,
    user_id: int,
    db_pool: DatabasePool,
):
    try:
        _tasks[task_id]["status"] = "running"
        # Execute report (this also saves execution record)
        result = ReportService.execute_report(report_id, db_pool, parameters)
        # The result contains the output (JSON string or bytes for Excel/PDF)
        output = result.get("output")
        # For JSON, output is a string; for Excel/PDF, it's bytes.
        # We'll store the output in the task result for download.
        _tasks[task_id]["status"] = "completed"
        _tasks[task_id]["result"] = {
            "format": format,
            "data": output if isinstance(output, str) else output.hex(),  # hex for bytes
            "is_binary": not isinstance(output, str),
        }
    except Exception as e:
        _tasks[task_id]["status"] = "failed"
        _tasks[task_id]["error"] = str(e)

@router.get("/status/{task_id}")
async def get_export_status(
    task_id: str,
    current_user: User = Depends(get_current_active_user),
):
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return _tasks[task_id]

@router.get("/download/{task_id}")
async def download_export(
    task_id: str,
    current_user: User = Depends(get_current_active_user),
):
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    task = _tasks[task_id]
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task not completed")
    result = task["result"]
    fmt = result["format"]
    data = result["data"]
    if result["is_binary"]:
        # Convert hex back to bytes
        import binascii
        content = binascii.unhexlify(data)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if fmt == "excel" else "application/pdf"
        filename = f"report.{'xlsx' if fmt == 'excel' else 'pdf'}"
        return StreamingResponse(
            iter([content]),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    else:
        # JSON
        return JSONResponse(content=json.loads(data))

# ---------- Direct export (sync) with streaming ----------
@router.get("/sync/{report_id}")
@limiter.limit("10/minute")
async def export_report_sync(
    request: Request,
    report_id: int,
    format: str = Query("excel", pattern="^(excel|pdf|json)$"),  # <-- FIX: regex → pattern
    current_user: User = Depends(get_current_active_user),
    db_pool: DatabasePool = Depends(get_db_pool),
):
    """
    Direct synchronous export. Returns the file immediately.
    For large exports, use the async endpoint.
    """
    try:
        result = ReportService.execute_report(report_id, db_pool, {})
        output = result["output"]
        if format == "json":
            return JSONResponse(content=json.loads(output))
        elif format == "excel":
            return StreamingResponse(
                iter([output]),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=report.xlsx"}
            )
        elif format == "pdf":
            return StreamingResponse(
                iter([output]),
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=report.pdf"}
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

# ---------- Cleanup (optional) ----------
# Could add a periodic task to clean up old task entries.
