from database.catalog.catalog_loader import CatalogLoader


class SemanticDiscovery:

    def __init__(self):

        self.catalog = CatalogLoader()

    # ---------------------------------------------------------

    def discover(self):

        semantic = []

        for table in self.catalog.tables():

            info = self.catalog.table(table)

            semantic.append({

                "table": table,

                "title": info.get("title", table),

                "description": info.get("description", ""),

                "keywords": info.get("keywords", [])

            })

        return semantic
