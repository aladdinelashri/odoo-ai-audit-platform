from database.catalog.catalog_loader import CatalogLoader


class RelationshipGraph:

    def __init__(self):

        self.catalog = CatalogLoader()

        self.graph = {}

        self.build()

    # ---------------------------------------------------------

    def build(self):

        catalog = self.catalog.load()

        for table, info in catalog.items():

            self.graph.setdefault(

                table,

                []

            )

            for relation in info.get(

                "relations",

                []

            ):

                self.graph[table].append(

                    {

                        "table": relation["target_table"],

                        "source_field": relation["source_field"],

                        "target_field": relation["target_field"]

                    }

                )

    # ---------------------------------------------------------

    def neighbors(self, table):

        return self.graph.get(

            table,

            []

        )
