from database.catalog.catalog_loader import CatalogLoader


class ModelDiscovery:

    def __init__(self):

        self.catalog = CatalogLoader()

    # ---------------------------------------------------------

    def discover(self):

        models = []

        for table in self.catalog.tables():

            info = self.catalog.table(table)

            models.append({

                "table": table,

                "columns": len(info["columns"]["columns"]),

                "description": info.get("description", "")

            })

        return models
