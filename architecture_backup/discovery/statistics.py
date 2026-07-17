from database.catalog.catalog_loader import CatalogLoader
from database.schema.relationship_graph import RelationshipGraph


class DiscoveryStatistics:

    def __init__(self):

        self.catalog = CatalogLoader()

        self.graph = RelationshipGraph()

    # ---------------------------------------------------------

    def collect(self):

        tables = self.catalog.tables()

        total_columns = 0

        for table in tables:

            info = self.catalog.table(table)

            total_columns += len(

                info["columns"]["columns"]

            )

        total_relations = 0

        for table in tables:

            total_relations += len(

                self.graph.from_table(table)

            )

        return {

            "tables": len(tables),

            "columns": total_columns,

            "relations": total_relations

        }
