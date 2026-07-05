import json
from pathlib import Path


class MetadataBuilder:

    def __init__(self):

        self.schema_path = Path("data/schema")

    def load(self, filename):

        with open(
            self.schema_path / filename,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def build(self):

        tables = self.load("tables.json")
        columns = self.load("columns.json")
        primary_keys = self.load("primary_keys.json")
        foreign_keys = self.load("foreign_keys.json")
        indexes = self.load("indexes.json")
        constraints = self.load("constraints.json")
        views = self.load("views.json")

        metadata = {}

        for table in tables:

            metadata[table] = {
                "table": table,
                "columns": columns.get(table, []),
                "primary_key": primary_keys.get(table, {}),
                "foreign_keys": foreign_keys.get(table, []),
                "indexes": indexes.get(table, []),
                "constraints": constraints.get(table, []),
                "is_view": table in views,
            }

        return metadata
