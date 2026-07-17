import json
from pathlib import Path

from sqlalchemy import text

from connectors.postgres.connection import PostgreSQLConnection


class ForeignKeysBuilder:

    def __init__(self):

        self.engine = PostgreSQLConnection().connect()

    def discover(self):

        sql = """
        SELECT

            tc.table_name,

            kcu.column_name,

            ccu.table_name AS foreign_table,

            ccu.column_name AS foreign_column

        FROM information_schema.table_constraints tc

        JOIN information_schema.key_column_usage kcu

            ON tc.constraint_name = kcu.constraint_name

        JOIN information_schema.constraint_column_usage ccu

            ON ccu.constraint_name = tc.constraint_name

        WHERE tc.constraint_type='FOREIGN KEY'

        ORDER BY tc.table_name;
        """

        with self.engine.connect() as conn:

            result = conn.execute(text(sql))

            return [

                dict(row._mapping)

                for row in result

            ]

    def build(self):

        data = self.discover()

        output = Path("database/schema/foreign_keys.json")

        with open(output, "w", encoding="utf-8") as f:

            json.dump(

                data,

                f,

                ensure_ascii=False,

                indent=4

            )

        print(f"Foreign Keys saved to {output}")


if __name__ == "__main__":

    ForeignKeysBuilder().build()
