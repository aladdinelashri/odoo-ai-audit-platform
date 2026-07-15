"""
Database Capabilities

Architecture V26
"""

from __future__ import annotations

from database.executor.postgres_executor import PostgreSQLExecutor


class DatabaseCapabilities:

    def __init__(
        self,
        executor: PostgreSQLExecutor,
    ) -> None:

        self.executor = executor

    # ---------------------------------------------------------

    def detect(self) -> dict:

        rows = self.executor.execute(
            """
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename;
            """
        )

        tables = [row[0] for row in rows]

        return {
            "tables": tables,
        }
