from database.schema.relationship_graph import RelationshipGraph


class RelationDiscovery:

    def __init__(self):

        self.graph = RelationshipGraph()

    # ---------------------------------------------------------

    def discover(self):

        relations = []

        for table in self.graph.tables():

            for relation in self.graph.from_table(table):

                relations.append({

                    "source_table": table,

                    "target_table": relation["target_table"],

                    "source_field": relation["source_field"],

                    "target_field": relation["target_field"]

                })

        return relations
