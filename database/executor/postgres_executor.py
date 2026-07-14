"""
PostgreSQL Executor

Architecture V11

Executes parameterized SQL queries against PostgreSQL.
"""

from __future__ import annotations

from typing import Any

import psycopg2


class PostgreSQLExecutor:

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
    ) -> None:

        self.connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password,
        )

    # ---------------------------------------------------------

    def execute(
        self,
        sql: str,
        params: list[Any] | None = None,
    ) -> list[tuple]:

        with self.connection.cursor() as cursor:

            cursor.execute(sql, params or [])

            try:
                return cursor.fetchall()
            except psycopg2.ProgrammingError:
                return []

    # ---------------------------------------------------------

    def close(self) -> None:

        self.connection.close()
