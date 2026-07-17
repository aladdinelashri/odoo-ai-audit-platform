"""
Query Executor

Architecture V11

Combines SQL safety validation with PostgreSQL execution.
"""

from __future__ import annotations

from typing import Any

from database.executor.postgres_executor import PostgreSQLExecutor
from database.executor.safe_executor import SafeExecutor


class QueryExecutor:

    def __init__(
        self,
        postgres: PostgreSQLExecutor,
    ) -> None:

        self.postgres = postgres
        self.safe = SafeExecutor()

    # ---------------------------------------------------------

    def execute(
        self,
        sql: str,
        params: list[Any] | None = None,
    ) -> list[tuple]:

        self.safe.validate(sql)

        return self.postgres.execute(sql, params)
