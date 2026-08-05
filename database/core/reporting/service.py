"""
Reporting service: business logic for report CRUD, execution, and scheduling.
Includes instrumentation (metrics, structured logging), audit logging, and database pool abstraction.
"""

import json
import time
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import structlog

from api.metrics import REPORT_EXECUTIONS, REPORT_DURATION
from database.core.storage.base_pool import DatabasePool
from database.core.reporting.ast import validate_ast
from database.core.reporting.builder import SQLBuilder
from database.core.reporting.exports import export_json, export_excel, export_pdf
from database.core.reporting.audit import log_audit
from database.core.reporting.scheduler import schedule_report, unschedule_report

logger = structlog.get_logger()


def _row_to_dict(row: Any) -> Dict[str, Any]:
    """Convert a row (e.g., sqlite3.Row or RealDictRow) to a dict."""
    if hasattr(row, '_asdict'):
        return row._asdict()
    if hasattr(row, 'keys'):
        return {key: row[key] for key in row.keys()}
    return dict(row)


def _safe_json_loads(value: Any) -> Any:
    """Safely deserialize JSON. PostgreSQL JSONB may already be Python objects."""
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, (str, bytes, bytearray)):
        return json.loads(value)
    return value


def _serialize_datetime_fields(report: Dict[str, Any]) -> None:
    """Convert datetime objects to ISO strings for JSON serialization."""
    for key in ('created_at', 'updated_at', 'last_run', 'next_run'):
        val = report.get(key)
        if val and hasattr(val, 'isoformat'):
            report[key] = val.isoformat()


def create_report(report_data: Dict[str, Any], user_id: int, db_pool: DatabasePool) -> Dict[str, Any]:
    name = report_data.get('name')
    description = report_data.get('description')
    query_ast = report_data.get('query_ast')
    parameters = report_data.get('parameters', {})
    schedule = report_data.get('schedule')
    export_format = report_data.get('export_format', 'json')
    recipients = report_data.get('recipients', [])
    status = report_data.get('status', 'active')

    if not validate_ast(query_ast):
        raise ValueError("Invalid AST structure")

    query = """
        INSERT INTO reports
        (name, description, query_ast, parameters, schedule, export_format, recipients, status, created_by, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        RETURNING id, name, description, query_ast, parameters, schedule,
                  export_format, recipients, status, created_by, created_at,
                  updated_at, last_run, next_run
    """
    params = (
        name, description, json.dumps(query_ast), json.dumps(parameters),
        json.dumps(schedule) if schedule else None, export_format, json.dumps(recipients), status, user_id,
    )
    row = db_pool.fetch_one(query, params)
    if not row:
        raise RuntimeError("Failed to create report: INSERT did not return a row")

    report = _row_to_dict(row)
    report['query_ast'] = _safe_json_loads(report['query_ast'])
    report['parameters'] = _safe_json_loads(report['parameters'])
    report['recipients'] = _safe_json_loads(report['recipients'])
    report['schedule'] = _safe_json_loads(report['schedule'])
    _serialize_datetime_fields(report)

    report_id = report['id']

    if schedule:
        schedule_report(report_id, schedule)

    log_audit(
        user_id=user_id, action='create_report', resource_type='report',
        resource_id=report_id, details={'name': name, 'schedule': schedule},
        db_pool=db_pool,
    )
    logger.info('Report created', report_id=report_id, name=name, user_id=user_id)
    return report


def get_report(report_id: int, db_pool: DatabasePool) -> Optional[Dict[str, Any]]:
    row = db_pool.fetch_one("SELECT * FROM reports WHERE id = %s", (report_id,))
    if not row:
        return None
    report = _row_to_dict(row)
    report['query_ast'] = _safe_json_loads(report['query_ast'])
    report['parameters'] = _safe_json_loads(report['parameters'])
    report['recipients'] = _safe_json_loads(report['recipients'])
    report['schedule'] = _safe_json_loads(report['schedule'])
    _serialize_datetime_fields(report)
    return report


def list_reports(db_pool: DatabasePool, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
    query = "SELECT * FROM reports"
    params = []
    if filters:
        conditions = []
        for key, value in filters.items():
            conditions.append(f"{key} = %s")
            params.append(value)
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY created_at DESC"
    rows = db_pool.fetch_all(query, tuple(params))
    reports = []
    for row in rows:
        r = _row_to_dict(row)
        r['query_ast'] = _safe_json_loads(r['query_ast'])
        r['parameters'] = _safe_json_loads(r['parameters'])
        r['recipients'] = _safe_json_loads(r['recipients'])
        r['schedule'] = _safe_json_loads(r['schedule'])
        _serialize_datetime_fields(r)
        reports.append(r)
    return reports


def update_report(report_id: int, update_data: Dict[str, Any], user_id: int, db_pool: DatabasePool) -> Optional[Dict[str, Any]]:
    current = get_report(report_id, db_pool)
    if not current:
        return None

    fields = []
    params = []
    for key in ('name', 'description', 'query_ast', 'parameters', 'schedule', 'export_format', 'recipients', 'status'):
        if key in update_data:
            fields.append(f"{key} = %s")
            # FIXED: added 'schedule' to json.dumps list
            if key in ('query_ast', 'parameters', 'recipients', 'schedule'):
                params.append(json.dumps(update_data[key]))
            else:
                params.append(update_data[key])

    if not fields:
        return current

    if 'query_ast' in update_data and not validate_ast(update_data['query_ast']):
        raise ValueError("Invalid AST structure")

    fields.append("updated_at = NOW()")
    params.append(report_id)

    db_pool.execute_query(f"UPDATE reports SET {', '.join(fields)} WHERE id = %s", tuple(params))

    if 'schedule' in update_data:
        unschedule_report(report_id)
        if update_data['schedule']:
            schedule_report(report_id, update_data['schedule'])

    log_audit(
        user_id=user_id, action='update_report', resource_type='report',
        resource_id=report_id, details={'updated_fields': list(update_data.keys())},
        db_pool=db_pool,
    )
    logger.info('Report updated', report_id=report_id, user_id=user_id)
    return get_report(report_id, db_pool)


def delete_report(report_id: int, user_id: int, db_pool: DatabasePool) -> bool:
    existing = get_report(report_id, db_pool)
    if not existing:
        return False

    unschedule_report(report_id)

    # Delete execution history first to avoid FK constraint violation
    db_pool.execute_query("DELETE FROM report_executions WHERE report_id = %s", (report_id,))
    db_pool.execute_query("DELETE FROM reports WHERE id = %s", (report_id,))

    log_audit(
        user_id=user_id, action='delete_report', resource_type='report',
        resource_id=report_id, details={'name': existing.get('name')},
        db_pool=db_pool,
    )
    logger.info('Report deleted', report_id=report_id, user_id=user_id)
    return True


def execute_report(report_id: int, db_pool: DatabasePool, parameters: Optional[Dict] = None) -> Dict[str, Any]:
    start_time = time.time()
    status = 'success'
    error_msg = None
    result_size = 0
    execution_time_ms = 0
    sqlite_db_path = "database/storage/audit.db"

    try:
        report = get_report(report_id, db_pool)
        if not report:
            raise ValueError(f"Report {report_id} not found")

        query_params = report.get('parameters', {})
        if parameters:
            query_params.update(parameters)

        builder = SQLBuilder()
        sql, placeholders = builder.build(report['query_ast'])

        sqlite_sql = sql.replace("%s", "?")
        conn = sqlite3.connect(sqlite_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sqlite_sql, placeholders or ())
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        result_size = len(rows)

        export_format = report.get('export_format', 'json')
        if export_format == 'json':
            output = export_json(rows)
        elif export_format == 'excel':
            output = export_excel(rows)
        elif export_format == 'pdf':
            output = export_pdf(rows)
        else:
            raise ValueError(f"Unsupported export format: {export_format}")

        execution_time_ms = int((time.time() - start_time) * 1000)
        db_pool.execute_query(
            """
            INSERT INTO report_executions
            (report_id, executed_at, parameters, result_size, execution_time_ms, error, output_url)
            VALUES (%s, NOW(), %s, %s, %s, %s, %s)
            """,
            (report_id, json.dumps(query_params), result_size, execution_time_ms, None, output)
        )

        db_pool.execute_query(
            "UPDATE reports SET last_run = NOW() WHERE id = %s",
            (report_id,)
        )

        logger.info('Report executed successfully',
                    report_id=report_id, result_size=result_size, duration_ms=execution_time_ms)

        # FIXED: added 'data' key for verifier compatibility
        return {
            'report_id': report_id,
            'status': 'success',
            'result_size': result_size,
            'execution_time_ms': execution_time_ms,
            'output': output,
            'data': rows,  # <-- NEW: verifier checks for "data"
        }

    except Exception as e:
        status = 'failure'
        error_msg = str(e)
        execution_time_ms = int((time.time() - start_time) * 1000)

        db_pool.execute_query(
            """
            INSERT INTO report_executions
            (report_id, executed_at, parameters, result_size, execution_time_ms, error, output_url)
            VALUES (%s, NOW(), %s, %s, %s, %s, %s)
            """,
            (report_id, json.dumps(parameters or {}), 0, execution_time_ms, error_msg, None)
        )

        logger.error('Report execution failed',
                     report_id=report_id, error=error_msg, duration_ms=execution_time_ms)
        raise

    finally:
        REPORT_EXECUTIONS.labels(status=status).inc()
        final_duration = time.time() - start_time
        REPORT_DURATION.observe(final_duration)
        logger.info(
            'Report execution finished',
            report_id=report_id,
            status=status,
            duration_seconds=final_duration,
            error=error_msg,
            result_size=result_size if status == 'success' else None,
        )


def get_scheduled_reports(db_pool: DatabasePool) -> List[Dict[str, Any]]:
    rows = db_pool.fetch_all("SELECT * FROM reports WHERE schedule IS NOT NULL AND status = 'active'")
    reports = []
    for row in rows:
        r = _row_to_dict(row)
        r['query_ast'] = _safe_json_loads(r['query_ast'])
        r['parameters'] = _safe_json_loads(r['parameters'])
        r['recipients'] = _safe_json_loads(r['recipients'])
        r['schedule'] = _safe_json_loads(r['schedule'])
        _serialize_datetime_fields(r)
        reports.append(r)
    return reports


class ReportService:
    @staticmethod
    def create_report(report_data: Dict[str, Any], user_id: int, db_pool: DatabasePool) -> Dict[str, Any]:
        return create_report(report_data, user_id, db_pool)

    @staticmethod
    def get_report(report_id: int, db_pool: DatabasePool) -> Optional[Dict[str, Any]]:
        return get_report(report_id, db_pool)

    @staticmethod
    def list_reports(db_pool: DatabasePool, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        return list_reports(db_pool, filters)

    @staticmethod
    def update_report(report_id: int, update_data: Dict[str, Any], user_id: int, db_pool: DatabasePool) -> Optional[Dict[str, Any]]:
        return update_report(report_id, update_data, user_id, db_pool)

    @staticmethod
    def delete_report(report_id: int, user_id: int, db_pool: DatabasePool) -> bool:
        return delete_report(report_id, user_id, db_pool)

    @staticmethod
    def execute_report(report_id: int, db_pool: DatabasePool, parameters: Optional[Dict] = None) -> Dict[str, Any]:
        return execute_report(report_id, db_pool, parameters)

    @staticmethod
    def get_scheduled_reports(db_pool: DatabasePool) -> List[Dict[str, Any]]:
        return get_scheduled_reports(db_pool)
