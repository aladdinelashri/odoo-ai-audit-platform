"""
SQL Executor

Production Engine V2
"""

from __future__ import annotations

from database.connection.postgres_connection import PostgreSQLConnection


class SQLExecutor:

    def __init__(self) -> None:

        self.database = PostgreSQLConnection()
        self.connection = None

    # ---------------------------------------------------------

    def execute(
        self,
        sql: str,
        params: list | None = None,
    ) -> list[dict]:

        params = params or []

        self.connection = self.database.open()

        with self.connection.cursor() as cursor:

            cursor.execute(sql, params)

            if cursor.description is None:
                return []

            columns = [c[0] for c in cursor.description]

            rows = cursor.fetchall()

            return [
                dict(zip(columns, row))
                for row in rows
            ]

    # ---------------------------------------------------------

    def close(self) -> None:

        if self.connection is not None:

            self.connection.close()

            self.connection = None

        self.database.close()
