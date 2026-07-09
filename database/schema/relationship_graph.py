import json
from pathlib import Path

from database.schema.schema_graph import SchemaGraph


class RelationshipGraph:

    def __init__(self):

        self.graph = SchemaGraph()

        self.loaded = False

    # ---------------------------------------------------------

    def load(self):

        if self.loaded:

            return

        file = Path("database/schema/model_relations.json")

        with open(file, encoding="utf-8") as f:

            relations = json.load(f)

        for relation in relations:

            self.graph.add_relation(

                relation["source_table"],
                relation["source_field"],
                relation["target_table"],
                relation["target_field"]

            )

        self.loaded = True

    # ---------------------------------------------------------

    def tables(self):

        self.load()

        return self.graph.all_tables()

    # ---------------------------------------------------------

    def from_table(self, table):

        self.load()

        return self.graph.from_table(table)

    # ---------------------------------------------------------

    def relation_count(self):

        self.load()

        return self.graph.relation_count()
