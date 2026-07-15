"""
Schema Loader

Architecture V15
"""

from __future__ import annotations

from database.executor.postgres_executor import PostgreSQLExecutor


class SchemaLoader:

    def __init__(self, executor: PostgreSQLExecutor):
        self.executor = executor

    # ---------------------------------------------------------

    def list_tables(self) -> list[str]:

        rows = self.executor.execute(
            """
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename;
            """
        )

        return [row[0] for row in rows]

    # ---------------------------------------------------------

    def list_columns(self, table: str) -> list[str]:

        rows = self.executor.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = %s
            ORDER BY ordinal_position;
            """,
            [table],
        )

        return [row[0] for row in rows]

    # ---------------------------------------------------------

    def primary_key(self, table: str) -> str | None:

        rows = self.executor.execute(
            """
            SELECT a.attname
            FROM pg_index i
            JOIN pg_attribute a
              ON a.attrelid = i.indrelid
             AND a.attnum = ANY(i.indkey)
            WHERE i.indrelid = %s::regclass
              AND i.indisprimary;
            """,
            [table],
        )

        if not rows:
            return None

        return rows[0][0]

    # ---------------------------------------------------------

    def foreign_keys(self, table: str) -> list[dict]:

        rows = self.executor.execute(
            """
            SELECT
                kcu.column_name,
                ccu.table_name AS referenced_table,
                ccu.column_name AS referenced_column
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_name = %s
            ORDER BY kcu.column_name;
            """,
            [table],
        )

        return [
            {
                "column": row[0],
                "referenced_table": row[1],
                "referenced_column": row[2],
            }
            for row in rows
        ]
