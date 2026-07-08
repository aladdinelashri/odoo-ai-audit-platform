import re

from database.catalog.catalog_loader import CatalogLoader
from database.catalog.column_index import ColumnIndex
from database.resolver.table_resolver import TableResolver

from database.ai.reasoning.business_dictionary import BUSINESS_TERMS


class EntityDetector:

    def __init__(self):

        self.loader = CatalogLoader()

        self.tables = TableResolver()

        self.columns = ColumnIndex()

        self.business = BUSINESS_TERMS

    # ---------------------------------------------------------

    def detect(self, text):

        original = text

        lowered = text.lower()

        entities = {

            "tables": [],

            "columns": []

        }

        # -------------------------------------------------
        # Business phrases (consume text)
        # -------------------------------------------------

        phrases = sorted(

            self.business.items(),

            key=lambda x: len(x[0]),

            reverse=True

        )

        consumed = lowered

        for phrase, table in phrases:

            p = phrase.lower()

            if p in consumed:

                if table not in entities["tables"]:

                    entities["tables"].append(table)

                consumed = consumed.replace(p, " ")

        # -------------------------------------------------
        # Remaining words
        # -------------------------------------------------

        words = re.findall(

            r"[A-Za-z0-9_]+",

            consumed

        )

        # -------------------------------------------------
        # Tables
        # -------------------------------------------------

        for word in words:

            if self.loader.exists(word):

                if word not in entities["tables"]:

                    entities["tables"].append(word)

                continue

            table = self.tables.resolve(word)

            if table:

                if table not in entities["tables"]:

                    entities["tables"].append(table)

        # -------------------------------------------------
        # Columns
        # -------------------------------------------------

        for word in re.findall(

            r"[A-Za-z0-9_]+",

            original

        ):

            if self.columns.exists(word):

                entities["columns"].append(

                    {

                        "name": word,

                        "tables": self.columns.tables(word)

                    }

                )

        return entities
