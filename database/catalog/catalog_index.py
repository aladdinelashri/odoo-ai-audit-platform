from database.catalog.catalog_loader import CatalogLoader


class CatalogIndex:

    def __init__(self):

        self.catalog = CatalogLoader()

        self.index = {}

        self.build()

    # ---------------------------------------------------------

    def build(self):

        self.index = {}

        for table in self.catalog.tables():

            info = self.catalog.table(table)

            columns = info["columns"]["columns"]

            for column in columns:

                name = column["column_name"]

                self.index.setdefault(name, [])

                self.index[name].append(table)

    # ---------------------------------------------------------

    def search(self, column):

        return self.index.get(column, [])

    # ---------------------------------------------------------

    def exists(self, column):

        return column in self.index

    # ---------------------------------------------------------

    def count(self):

        return len(self.index)
