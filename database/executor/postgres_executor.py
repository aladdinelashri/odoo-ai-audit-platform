"""
PostgreSQL Executor

Architecture V27
"""

from __future__ import annotations

from typing import Any

import psycopg2

from database.config.settings import settings


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

    @classmethod
    def from_config(cls) -> "PostgreSQLExecutor":

        db = settings.database

        return cls(
            host=db.host,
            port=db.port,
            database=db.database,
            user=db.user,
            password=db.password,
        )

    # ---------------------------------------------------------

    def execute(
        self,
        sql: str,
        params: list[Any] | None = None,
    ) -> list[tuple]:

        with self.connection.cursor() as cursor:

            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)

            try:
                return cursor.fetchall()
            except psycopg2.ProgrammingError:
                return []

    # ---------------------------------------------------------

    def execute_with_columns(
        self,
        sql: str,
        params: list[Any] | None = None,
    ) -> tuple[list[str], list[tuple]]:

        with self.connection.cursor() as cursor:

            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)

            columns = [desc[0] for desc in cursor.description]

            try:
                rows = cursor.fetchall()
            except psycopg2.ProgrammingError:
                rows = []

            return columns, rows

    # ---------------------------------------------------------

    def close(self) -> None:

        self.connection.close()
