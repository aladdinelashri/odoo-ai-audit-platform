import json
from pathlib import Path


class SchemaExporter:

    def __init__(self):
        self.output = Path("data/schema")
        self.output.mkdir(parents=True, exist_ok=True)

    def _save(self, filename, data):
        with open(
            self.output / filename,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(data, f, indent=4)

    def export_tables(self, tables):
        self._save("tables.json", tables)
        print(f"Saved {len(tables)} tables")
        print(self.output / "tables.json")

    def export_columns(self, columns):
        self._save("columns.json", columns)
        print(f"Saved columns for {len(columns)} tables")
        print(self.output / "columns.json")

    def export_primary_keys(self, primary_keys):
        self._save("primary_keys.json", primary_keys)
        print(f"Saved primary keys for {len(primary_keys)} tables")
        print(self.output / "primary_keys.json")

    def export_foreign_keys(self, foreign_keys):
        self._save("foreign_keys.json", foreign_keys)
        print(f"Saved foreign keys for {len(foreign_keys)} tables")
        print(self.output / "foreign_keys.json")

    def export_indexes(self, indexes):
        self._save("indexes.json", indexes)
        print(f"Saved indexes for {len(indexes)} tables")
        print(self.output / "indexes.json")

    def export_constraints(self, constraints):
        self._save("constraints.json", constraints)
        print(f"Saved constraints for {len(constraints)} tables")
        print(self.output / "constraints.json")

    def export_views(self, views):
        self._save("views.json", views)
        print(f"Saved {len(views)} views")
        print(self.output / "views.json")
