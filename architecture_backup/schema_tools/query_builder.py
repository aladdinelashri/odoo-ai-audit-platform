from database.schema.schema_index import SchemaIndex


class QueryBuilder:

    def __init__(self):

        self.schema = SchemaIndex()

    def select(self, table, columns):

        if not self.schema.exists(table):
            raise Exception(f"Unknown table: {table}")

        sql = "SELECT\n"

        sql += ",\n".join(columns)

        sql += f"\nFROM {table}"

        return sql

    def select_all(self, table):

        cols = [

            c["column_name"]

            for c in self.schema.columns(table)

        ]

        return self.select(table, cols)
