# service.py
import json
import time
from typing import Dict, Any, List, Optional
from database.core.storage.sqlite.sqlite_pool import SQLitePool
from database.core.reporting.builder import SQLBuilder
from database.core.reporting.ast import QueryAST


class ReportService:
    @staticmethod
    def create_report(
        name: str,
        query_ast: Dict[str, Any],
        description: Optional[str] = None,
        parameters: Optional[List[Dict]] = None,
        schedule: Optional[str] = None,
        export_format: str = "json",
        recipients: Optional[List[str]] = None,
    ) -> int:
        """Create a new report definition."""
        QueryAST.validate(query_ast)
        conn = SQLitePool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO reports
            (name, description, query_ast, parameters, schedule, export_format, recipients, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                description,
                json.dumps(query_ast),
                json.dumps(parameters or []),
                schedule,
                export_format,
                json.dumps(recipients or []),
                "draft",
            ),
        )
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def get_report(report_id: int) -> Optional[Dict[str, Any]]:
        conn = SQLitePool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
        row = cursor.fetchone()
        if not row:
            return None
        # Convert sqlite3.Row to dict
        report = dict(row)
        # Parse JSON fields
        report["query_ast"] = json.loads(report["query_ast"])
        report["parameters"] = json.loads(report["parameters"]) if report["parameters"] else []
        report["recipients"] = json.loads(report["recipients"]) if report["recipients"] else []
        return report

    @staticmethod
    def list_reports(status: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = SQLitePool.get_connection()
        cursor = conn.cursor()
        if status:
            cursor.execute("SELECT * FROM reports WHERE status = ?", (status,))
        else:
            cursor.execute("SELECT * FROM reports")
        rows = cursor.fetchall()
        reports = []
        for row in rows:
            r = dict(row)
            r["query_ast"] = json.loads(r["query_ast"])
            r["parameters"] = json.loads(r["parameters"]) if r["parameters"] else []
            r["recipients"] = json.loads(r["recipients"]) if r["recipients"] else []
            reports.append(r)
        return reports

    @staticmethod
    def update_report(report_id: int, **kwargs) -> bool:
        """Update report fields. Accepts any key from the reports table."""
        allowed = {"name", "description", "query_ast", "parameters", "schedule",
                   "export_format", "recipients", "status"}
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if not updates:
            return False
        # Convert dicts to JSON
        if "query_ast" in updates:
            updates["query_ast"] = json.dumps(updates["query_ast"])
        if "parameters" in updates:
            updates["parameters"] = json.dumps(updates["parameters"])
        if "recipients" in updates:
            updates["recipients"] = json.dumps(updates["recipients"])
        # Build SET clause
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [report_id]
        conn = SQLitePool.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE reports SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", values)
        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def delete_report(report_id: int) -> bool:
        conn = SQLitePool.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reports WHERE id = ?", (report_id,))
        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def execute_report(report_id: int, param_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a report by ID. For now, param_values are ignored because the AST contains literal values.
        In the future, we can replace placeholders in the AST with param_values.
        """
        report = ReportService.get_report(report_id)
        if not report:
            raise ValueError(f"Report with id {report_id} not found")

        ast = report["query_ast"]
        sql, params = SQLBuilder.ast_to_sql(ast)

        # Execute with timing
        start = time.perf_counter()
        try:
            rows = SQLitePool.execute(sql, params)
            elapsed_ms = (time.perf_counter() - start) * 1000

            # Log execution
            conn = SQLitePool.get_connection()
            conn.execute(
                """
                INSERT INTO report_executions
                (report_id, parameters, result_size, execution_time_ms)
                VALUES (?, ?, ?, ?)
                """,
                (report_id, json.dumps(param_values or {}), len(rows), elapsed_ms),
            )
            conn.commit()

            return {
                "data": rows,
                "row_count": len(rows),
                "execution_time_ms": elapsed_ms,
                "report_name": report["name"],
                "report_id": report_id,
            }
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start) * 1000
            conn = SQLitePool.get_connection()
            conn.execute(
                """
                INSERT INTO report_executions
                (report_id, parameters, error, execution_time_ms)
                VALUES (?, ?, ?, ?)
                """,
                (report_id, json.dumps(param_values or {}), str(e), elapsed_ms),
            )
            conn.commit()
            raise
