"""
AI Query Orchestrator

Architecture V22
"""

from __future__ import annotations

from database.ai.pipeline.ai_pipeline import AIPipeline
from database.security.sql_guard import SQLGuard
from database.executor.postgres_executor import PostgreSQLExecutor


class QueryOrchestrator:

    def __init__(
        self,
        pipeline: AIPipeline,
        guard: SQLGuard,
        executor: PostgreSQLExecutor,
    ) -> None:

        self.pipeline = pipeline
        self.guard = guard
        self.executor = executor

    # ---------------------------------------------------------

    def ask(self, text: str) -> dict:

        result = self.pipeline.analyze(text)

        model = result["model"]
        sql = result["sql"]
        params = result.get("params", [])

        if not self.guard.validate(model, sql):
            raise RuntimeError("SQL validation failed.")

        rows = self.executor.execute(sql, params)

        return {
            "model": model,
            "sql": sql,
            "rows": rows,
            "count": len(rows),
        }
