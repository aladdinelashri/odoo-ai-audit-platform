import json
from pathlib import Path

from database.schema.table_registry import TableRegistry


class RelationshipBuilder:

    def __init__(self):

        self.registry = TableRegistry()

    def discover(self):

        relations = []

        for table in self.registry.tables():

            for column in self.registry.columns(table):

                name = column["column_name"]

                if name.endswith("_id"):

                    target = name[:-3]

                    relations.append({

                        "table": table,

                        "column": name,

                        "target": target

                    })

        return relations

    def build(self):

        output = Path("database/schema/relationships.json")

        with open(output, "w", encoding="utf-8") as f:

            json.dump(

                self.discover(),

                f,

                ensure_ascii=False,

                indent=4

            )

        print(f"Relationships saved to {output}")


if __name__ == "__main__":

    RelationshipBuilder().build()
