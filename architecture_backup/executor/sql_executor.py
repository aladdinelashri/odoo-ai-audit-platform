"""
SQL Executor

Architecture V41

Executes SQL against PostgreSQL.
"""

from __future__ import annotations

from database.connection.postgres_connection import PostgreSQLConnection


class SQLExecutor:

    def __init__(self) -> None:

        self.connection = PostgreSQLConnection()

    def execute(
        self,
        sql: str,
        params: list,
    ) -> tuple[list[str], list[tuple]]:

        conn = self.connection.open()

        try:

            with conn.cursor() as cursor:

                cursor.execute(sql, params)

                rows = cursor.fetchall()

                columns = [
                    column.name
                    for column in cursor.description
                ]

                return columns, rows

        finally:

            self.connection.close()
