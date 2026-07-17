from database.catalog.catalog_loader import CatalogLoader


class CatalogSearch:

    def __init__(self):

        self.catalog = CatalogLoader()

    # ---------------------------------------------------------

    def table(self, name):

        return self.catalog.table(name)

    # ---------------------------------------------------------

    def column(self, table, column):

        info = self.catalog.table(table)

        if not info:

            return None

        columns = info["columns"]["columns"]

        for item in columns:

            if item["column_name"] == column:

                return item

        return None

    # ---------------------------------------------------------

    def columns(self, table):

        info = self.catalog.table(table)

        if not info:

            return []

        return info["columns"]["columns"]

    # ---------------------------------------------------------

    def relations(self, table):

        info = self.catalog.table(table)

        if not info:

            return []

        return info["relations"]
