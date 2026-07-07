import json
from pathlib import Path


class TableRegistry:

    def __init__(self):

        schema_file = Path("database/schema/schema.json")

        with open(schema_file, encoding="utf-8") as f:

            self.schema = json.load(f)

    def tables(self):

        return sorted(self.schema.keys())

    def exists(self, table):

        return table in self.schema

    def columns(self, table):

        return self.schema.get(table, [])

    def has_column(self, table, column):

        return any(
            c["column_name"] == column
            for c in self.columns(table)
        )

    def column_type(self, table, column):

        for c in self.columns(table):

            if c["column_name"] == column:

                return c["data_type"]

        return None
