from database.catalog.catalog_loader import CatalogLoader


class TableIndex:

    def __init__(self):

        self.catalog = CatalogLoader()

        self.index = {}

        self.build()

    # ---------------------------------------------------------

    def build(self):

        self.index = {}

        for table in self.catalog.tables():

            self.index[table.lower()] = table

    # ---------------------------------------------------------

    def exists(self, table):

        return table.lower() in self.index

    # ---------------------------------------------------------

    def resolve(self, table):

        return self.index.get(table.lower())

    # ---------------------------------------------------------

    def all(self):

        return list(self.index.keys())

    # ---------------------------------------------------------

    def count(self):

        return len(self.index)
