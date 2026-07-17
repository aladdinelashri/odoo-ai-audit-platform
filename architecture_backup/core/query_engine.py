"""
Query Engine

Production Engine V3
"""

from __future__ import annotations

from database.execution.sql_executor import SQLExecutor
from database.response.result_formatter import ResultFormatter


class QueryEngine:

    def __init__(self) -> None:

        self.executor = SQLExecutor()
        self.formatter = ResultFormatter()

    # ---------------------------------------------------------

    def execute(
        self,
        sql: str,
        params: list | None = None,
    ) -> dict:

        rows = self.executor.execute(
            sql,
            params,
        )

        return self.formatter.format(rows)
