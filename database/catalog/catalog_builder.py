import json
from pathlib import Path

from database.schema.schema_index import SchemaIndex


class CatalogBuilder:

    def __init__(self):

        self.db = SchemaIndex()

    def build(self):

        catalog = {}

        for table in self.db.table_names():

            catalog[table] = {

                "columns": self.db.columns(table),

                "relations": self.db.relations_from(table)

            }

        output = Path("database/catalog/catalog.json")

        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                catalog,
                f,
                ensure_ascii=False,
                indent=4
            )

        print()
        print("=" * 70)
        print("Catalog Builder")
        print("=" * 70)
        print()
        print(f"Tables : {len(catalog)}")
        print(f"Saved  : {output}")
        print()

        return catalog


if __name__ == "__main__":

    CatalogBuilder().build()
