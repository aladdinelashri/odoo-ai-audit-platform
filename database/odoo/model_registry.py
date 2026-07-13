from sqlalchemy import text

from connectors.postgres.connection import PostgreSQLConnection


class ModelRegistry:

    def __init__(self):

        self.engine = PostgreSQLConnection().connect()

    # ---------------------------------------------------------

    def models(self):

        sql = text("""

            SELECT

                model,

                name

            FROM ir_model

            ORDER BY model

        """)

        with self.engine.connect() as conn:

            rows = conn.execute(sql)

            return [

                dict(row._mapping)

                for row in rows

            ]
