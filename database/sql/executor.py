from sqlalchemy import text

from connectors.postgres.connection import PostgreSQLConnection


class SQLExecutor:

    def __init__(self):

        self.connection = PostgreSQLConnection()

        self.engine = self.connection.connect()

    def execute(self, sql, parameters=None):

        with self.engine.connect() as conn:

            result = conn.execute(
                text(sql),
                parameters or {}
            )

            return [
                dict(row._mapping)
                for row in result
            ]
