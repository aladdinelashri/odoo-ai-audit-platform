import json
from pathlib import Path

from database.catalog.catalog_loader import CatalogLoader
from database.catalog.column_index import ColumnIndex
from database.resolver.table_resolver import TableResolver


class EntityDetector:

    def __init__(self):

        self.loader = CatalogLoader()
        self.tables = TableResolver()
        self.columns = ColumnIndex()

        self.business = self.load_business_terms()

    # ---------------------------------------------------------

    def load_business_terms(self):

        path = (
            Path(__file__).parent
            / "vocabulary"
            / "business_terms.json"
        )

        with open(path, "r", encoding="utf-8") as f:

            return json.load(f)

    # ---------------------------------------------------------

    def detect(self, text):

        text = text.lower()

        entities = {

            "tables": [],

            "columns": []

        }

        consumed = set()

        # -------------------------------------------------
        # Business vocabulary (longest match first)
        # -------------------------------------------------

        terms = sorted(

            self.business.items(),

            key=lambda x: len(x[0]),

            reverse=True

        )

        for phrase, table in terms:

            if phrase.lower() in text:

                if table not in entities["tables"]:

                    entities["tables"].append(table)

                consumed.add(phrase.lower())

        # -------------------------------------------------

        words = text.split()

        # Direct table names

        for word in words:

            if word in consumed:

                continue

            if self.loader.exists(word):

                if word not in entities["tables"]:

                    entities["tables"].append(word)

                consumed.add(word)

        # Alias names

        for word in words:

            if word in consumed:

                continue

            table = self.tables.resolve(word)

            if table:

                if table not in entities["tables"]:

                    entities["tables"].append(table)

                consumed.add(word)

        # Columns

        for word in words:

            if word in consumed:

                continue

            if self.columns.exists(word):

                entities["columns"].append({

                    "name": word,

                    "tables": self.columns.tables(word)

                })

        return entities
