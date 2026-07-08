from database.catalog.catalog_loader import CatalogLoader


class ColumnIndex:

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

                name = column["column_name"].lower()

                if name not in self.index:

                    self.index[name] = []

                self.index[name].append({

                    "table": table,

                    "type": column["data_type"]

                })

    # ---------------------------------------------------------

    def exists(self, column):

        return column.lower() in self.index

    # ---------------------------------------------------------

    def search(self, column):

        return self.index.get(column.lower(), [])

    # ---------------------------------------------------------

    def count(self):

        return len(self.index)

    # ---------------------------------------------------------

    def tables(self, column):

        return [

            item["table"]

            for item in self.search(column)

        ]
