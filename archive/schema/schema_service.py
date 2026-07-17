import json
from pathlib import Path


class SchemaService:

    def __init__(self):

        base = Path("database/schema")

        with open(base / "schema.json", encoding="utf-8") as f:
            self.schema = json.load(f)

        with open(base / "foreign_keys.json", encoding="utf-8") as f:
            self.foreign_keys = json.load(f)

    def tables(self):

        return list(self.schema.keys())

    def columns(self, table):

        return self.schema.get(table, [])

    def has_table(self, table):

        return table in self.schema

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

    def relations(self, table):

        return [

            r for r in self.foreign_keys

            if r["table_name"] == table

        ]
