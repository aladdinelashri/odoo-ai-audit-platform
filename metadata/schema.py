from sqlalchemy import text

from connectors.postgres.connection import PostgreSQLConnection


class OdooSchema:

    def __init__(self):

        self.engine = PostgreSQLConnection().connect()

    def columns(self, table_name):

        sql = """
        SELECT
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_name = :table
        ORDER BY ordinal_position
        """

        with self.engine.connect() as conn:

            result = conn.execute(
                text(sql),
                {"table": table_name}
            )

            return [
                dict(row._mapping)
                for row in result
            ]

    def column_type(self, table_name, column_name):

        for column in self.columns(table_name):

            if column["column_name"] == column_name:

                return column["data_type"]

        return None

    def is_jsonb(self, table_name, column_name):

        return self.column_type(table_name, column_name) == "jsonb"

    def is_varchar(self, table_name, column_name):

        return self.column_type(table_name, column_name) == "character varying"

    def jsonb_columns(self, table_name):

        return [

            column["column_name"]

            for column in self.columns(table_name)

            if column["data_type"] == "jsonb"

        ]

    def has_column(self, table_name, column_name):

        return any(

            column["column_name"] == column_name

            for column in self.columns(table_name)

        )

    def print(self, table_name):

        print()

        print("=" * 70)
        print(table_name)
        print("=" * 70)
        print()

        for column in self.columns(table_name):

            print(
                f"{column['column_name']:<30}"
                f"{column['data_type']}"
            )
