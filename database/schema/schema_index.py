import json
from pathlib import Path


class SchemaIndex:

    def __init__(self):

        base = Path("database/schema")

        with open(base / "schema.json", encoding="utf-8") as f:
            self.tables = json.load(f)

        with open(base / "model_relations.json", encoding="utf-8") as f:
            self.relations = json.load(f)

    def table(self, table):

        return self.tables.get(table, {})

    def columns(self, table):

        return self.table(table).get("columns", [])

    def exists(self, table):

        return table in self.tables

    def column_type(self, table, column):

        for c in self.columns(table):

            if c["column_name"] == column:
                return c["data_type"]

        return None

    def has_column(self, table, column):

        return self.column_type(table, column) is not None

    def relations_from(self, table):

        return [

            r

            for r in self.relations

            if r["source_table"] == table

        ]

    def relations_to(self, table):

        return [

            r

            for r in self.relations

            if r["target_table"] == table

        ]
