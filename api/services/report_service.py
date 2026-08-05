"""Report service with execution and delivery logic."""
import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.models.models import Report, ReportExecution, User
from api.core.ast_validator import validate_query_ast, ast_to_sql
from api.services.email_service import deliver_report_email

logger = logging.getLogger(__name__)


def _serialize_datetime_fields(obj: Any) -> Any:
    """Recursively convert datetime objects to ISO strings."""
    if isinstance(obj, dict):
        return {k: _serialize_datetime_fields(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_serialize_datetime_fields(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    return obj


def create_report(db: Session, data: dict, owner_id: int) -> Report:
    """Create a new report."""
    # Validate AST before saving
    if "query_ast" in data:
        validate_query_ast(data["query_ast"])
    
    report = Report(
        name=data.get("name"),
        description=data.get("description"),
        query_ast=data.get("query_ast"),
        schedule=data.get("schedule"),
        recipients=data.get("recipients", []),
        status=data.get("status", "active"),
        owner_id=owner_id
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_report(db: Session, report_id: int, user_id: Optional[int] = None) -> Optional[Report]:
    """Get a report by ID."""
    query = db.query(Report).filter(Report.id == report_id)
    if user_id is not None:
        query = query.filter(Report.owner_id == user_id)
    return query.first()


def list_reports(db: Session, user_id: int, status_filter: Optional[str] = None) -> List[Report]:
    """List reports for a user."""
    query = db.query(Report).filter(Report.owner_id == user_id)
    if status_filter:
        query = query.filter(Report.status == status_filter)
    return query.order_by(Report.created_at.desc()).all()


def update_report(db: Session, report_id: int, data: dict, user_id: int) -> Optional[Report]:
    """Update a report."""
    report = get_report(db, report_id, user_id)
    if not report:
        return None
    
    if "query_ast" in data:
        validate_query_ast(data["query_ast"])
    
    for field in ["name", "description", "query_ast", "schedule", "recipients", "status"]:
        if field in data:
            setattr(report, field, data[field])
    
    db.commit()
    db.refresh(report)
    return report


def delete_report(db: Session, report_id: int, user_id: int) -> None:
    """Delete a report, ensuring executions are deleted first to avoid FK violations."""
    report = get_report(db, report_id, user_id)
    if not report:
        raise ValueError("Report not found")
    
    # Explicitly delete executions first to avoid FK violations
    db.query(ReportExecution).filter(ReportExecution.report_id == report_id).delete()
    db.delete(report)
    db.commit()


def execute_report(db: Session, sqlite_db: Session, report: Report, triggered_by: str = "manual") -> dict:
    """Execute a report query and optionally deliver via email."""
    execution = ReportExecution(
        report_id=report.id,
        status="running",
        triggered_by=triggered_by
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)
    
    try:
        # Validate and convert AST to SQL
        validate_query_ast(report.query_ast)
        sql, params = ast_to_sql(report.query_ast)
        
        # Execute against SQLite
        result = sqlite_db.execute(text(sql), params)
        rows = result.mappings().all()
        data = [dict(row) for row in rows]
        
        # Update execution success
        execution.status = "completed"
        execution.completed_at = datetime.now(timezone.utc)
        execution.result_count = len(data)
        execution.result_preview = data[:10]  # Store first 10 rows as preview
        
        db.commit()
        
        # Priority 2: Email Delivery Integration
        # Hook _deliver_report into execute_report after successful query execution
        _deliver_report(db, execution, report, data)
        
        return {
            "execution_id": execution.id,
            "status": execution.status,
            "result_count": len(data),
            "data": data,
            "delivery_status": execution.delivery_status,
            "delivery_error": execution.delivery_error
        }
        
    except Exception as e:
        logger.error(f"Report execution failed: {e}")
        execution.status = "failed"
        execution.completed_at = datetime.now(timezone.utc)
        execution.error_message = str(e)
        db.commit()
        raise


def _deliver_report(db: Session, execution: ReportExecution, report: Report, data: List[Dict[str, Any]]) -> None:
    """Deliver report to configured recipients via email."""
    recipients = report.recipients or []
    if not recipients:
        execution.delivery_status = "no_recipients"
        db.commit()
        return
    
    # For delivery, we create a simple JSON attachment
    import json
    attachment_data = json.dumps(data, indent=2, default=str).encode("utf-8")
    attachment_filename = f"{report.name.replace(' ', '_')}_exec_{execution.id}.json"
    
    result = deliver_report_email(
        recipients=recipients,
        report_name=report.name,
        execution_id=execution.id,
        attachment_data=attachment_data,
        attachment_filename=attachment_filename,
        attachment_mimetype="application/json"
    )
    
    if result["success"]:
        execution.delivery_status = "delivered"
        execution.delivery_error = None
    else:
        execution.delivery_status = "failed"
        execution.delivery_error = result["error"]
    
    db.commit()


def trigger_report(db: Session, sqlite_db: Session, report_id: int, user_id: Optional[int], triggered_by: str = "manual") -> dict:
    """Trigger a report execution synchronously (returns 200 with data)."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise ValueError("Report not found")
    
    if user_id is not None and report.owner_id != user_id:
        raise ValueError("Unauthorized")
    
    return execute_report(db, sqlite_db, report, triggered_by)


def get_report_executions(db: Session, report_id: int, user_id: int) -> List[ReportExecution]:
    """Get execution history for a report."""
    report = get_report(db, report_id, user_id)
    if not report:
        return []
    return db.query(ReportExecution).filter(ReportExecution.report_id == report_id).order_by(ReportExecution.started_at.desc()).all()
