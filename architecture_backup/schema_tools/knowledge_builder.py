import json
from pathlib import Path

from database.schema.table_registry import TableRegistry


class KnowledgeBuilder:

    def __init__(self):

        self.registry = TableRegistry()

    def build(self):

        knowledge = {}

        for table in self.registry.tables():

            knowledge[table] = {

                "columns": [

                    {

                        "name": c["column_name"],

                        "type": c["data_type"]

                    }

                    for c in self.registry.columns(table)

                ],

                "jsonb_columns": [

                    c["column_name"]

                    for c in self.registry.columns(table)

                    if c["data_type"] == "jsonb"

                ]

            }

        output = Path("database/schema/knowledge.json")

        with open(output, "w", encoding="utf-8") as f:

            json.dump(

                knowledge,

                f,

                ensure_ascii=False,

                indent=4

            )

        print(f"Knowledge saved to {output}")


if __name__ == "__main__":

    KnowledgeBuilder().build()
