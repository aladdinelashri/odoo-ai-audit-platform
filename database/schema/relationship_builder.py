import json
from pathlib import Path

from database.schema.table_registry import TableRegistry


class RelationshipBuilder:

    def __init__(self):

        self.registry = TableRegistry()

    # ---------------------------------------------------------

    def discover(self):

        relations = []

        for table in self.registry.tables():

            columns = self.registry.columns(table)

            for column in columns:

                if isinstance(column, str):

                    name = column

                else:

                    name = column["column_name"]

                if not name.endswith("_id"):

                    continue

                relations.append({

                    "source_table": table,

                    "source_field": name,

                    "target_table": name[:-3],

                    "target_field": "id"

                })

        return relations

    # ---------------------------------------------------------

    def build(self):

        relations = self.discover()

        output = Path("database/schema/relationships.json")

        with open(output, "w", encoding="utf-8") as f:

            json.dump(

                relations,

                f,

                ensure_ascii=False,

                indent=4

            )

        print(f"Relationships saved to {output}")

        return relations


if __name__ == "__main__":

    RelationshipBuilder().build()
