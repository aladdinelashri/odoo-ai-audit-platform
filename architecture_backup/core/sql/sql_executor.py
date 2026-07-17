"""
Core SQL Executor

Architecture V3
"""

from __future__ import annotations

from database.core.pipeline.context import PipelineContext
from database.sql.connection import DatabaseConnection


class SQLExecutor:

    def __init__(self):

        self.db = DatabaseConnection()

    # ---------------------------------------------------------

    def execute(self, context: PipelineContext):

        sql = context.sql
        parameters = context.sql_parameters

        connection = self.db.open()
        cursor = connection.cursor()

        try:

            cursor.execute(sql, parameters)

            columns = [c[0] for c in cursor.description]

            rows = [

                dict(zip(columns, row))

                for row in cursor.fetchall()

            ]

            context.rows = rows

            context.add_metadata(

                "rows_returned",

                len(rows),

            )

            return rows

        finally:

            cursor.close()

            connection.close()
