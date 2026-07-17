import json
from pathlib import Path


class CatalogLoader:

    def __init__(self):

        self.catalog = None

    # ---------------------------------------------------------

    def load(self):

        if self.catalog is not None:

            return self.catalog

        path = Path("database/catalog/catalog.json")

        with open(path, encoding="utf-8") as f:

            self.catalog = json.load(f)

        return self.catalog

    # ---------------------------------------------------------

    def tables(self):

        return self.load().keys()

    # ---------------------------------------------------------

    def table(self, table):

        return self.load().get(table)

    # ---------------------------------------------------------

    def exists(self, table):

        return table in self.load()
