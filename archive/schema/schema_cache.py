from sqlalchemy import text

from connectors.postgres.connection import PostgreSQLConnection


class SchemaCache:

    def __init__(self):

        self.engine = PostgreSQLConnection().connect()

        self.cache = {}

    def load(self):

        sql = """
        SELECT

            table_name,
            column_name,
            data_type

        FROM information_schema.columns

        WHERE table_schema='public'

        ORDER BY table_name, ordinal_position
        """

        with self.engine.connect() as conn:

            result = conn.execute(text(sql))

            self.cache = {}

            for row in result:

                row = dict(row._mapping)

                table = row["table_name"]

                if table not in self.cache:

                    self.cache[table] = {
                        "table": table,
                        "columns": []
                    }

                self.cache[table]["columns"].append(
                    {
                        "column_name": row["column_name"],
                        "data_type": row["data_type"]
                    }
                )

        return self.cache

    def tables(self):

        if not self.cache:
            self.load()

        return sorted(self.cache.keys())

    def columns(self, table):

        if not self.cache:
            self.load()

        if table not in self.cache:
            return []

        return self.cache[table]["columns"]

    def jsonb_columns(self, table):

        return [

            c["column_name"]

            for c in self.columns(table)

            if c["data_type"] == "jsonb"

        ]

    def column_type(self, table, column):

        for c in self.columns(table):

            if c["column_name"] == column:

                return c["data_type"]

        return None

    def is_jsonb(self, table, column):

        return self.column_type(table, column) == "jsonb"
