from database.catalog.catalog_loader import CatalogLoader


class CatalogTypes:

    NUMERIC_TYPES = {

        "integer",
        "bigint",
        "smallint",
        "numeric",
        "decimal",
        "real",
        "double precision"

    }

    DATE_TYPES = {

        "date",
        "timestamp without time zone",
        "timestamp with time zone"

    }

    TEXT_TYPES = {

        "character varying",
        "character",
        "text",
        "json",
        "jsonb"

    }

    # ---------------------------------------------------------

    def __init__(self):

        self.catalog = CatalogLoader()

    # ---------------------------------------------------------

    def _columns(self, table):

        info = self.catalog.table(table)

        return info["columns"]["columns"]

    # ---------------------------------------------------------

    def numeric(self, table):

        return [

            c["column_name"]

            for c in self._columns(table)

            if c["data_type"] in self.NUMERIC_TYPES

        ]

    # ---------------------------------------------------------

    def dates(self, table):

        return [

            c["column_name"]

            for c in self._columns(table)

            if c["data_type"] in self.DATE_TYPES

        ]

    # ---------------------------------------------------------

    def text(self, table):

        return [

            c["column_name"]

            for c in self._columns(table)

            if c["data_type"] in self.TEXT_TYPES

        ]
