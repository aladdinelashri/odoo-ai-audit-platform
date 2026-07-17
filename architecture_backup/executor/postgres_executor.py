"""
PostgreSQL Executor

Architecture V71
"""

from __future__ import annotations

from typing import Any

import psycopg2

from database.config.settings import settings


class PostgreSQLExecutor:

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        database: str | None = None,
        user: str | None = None,
        password: str | None = None,
    ) -> None:

        if host is None:

            db = settings.database

            host = db.host
            port = db.port
            database = db.database
            user = db.user
            password = db.password

        self.connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password,
        )

    @classmethod
    def from_config(cls) -> "PostgreSQLExecutor":

        return cls()

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

    def execute_with_columns(
        self,
        sql: str,
        params: list[Any] | None = None,
    ) -> tuple[list[str], list[tuple]]:

        with self.connection.cursor() as cursor:

            cursor.execute(sql, params or [])

            columns = [c[0] for c in cursor.description]

            try:
                rows = cursor.fetchall()
            except psycopg2.ProgrammingError:
                rows = []

            return columns, rows

    # ---------------------------------------------------------

    def close(self) -> None:

        self.connection.close()
