"""
Metadata Loader

Architecture V51
"""

from __future__ import annotations

from database.connection.postgres_connection import PostgreSQLConnection


class MetadataLoader:

    def __init__(self) -> None:

        self.database = PostgreSQLConnection()

    # ---------------------------------------------------------

    def _normalize_name(self, value):

        if isinstance(value, dict):

            if "en_US" in value:
                return value["en_US"]

            return next(iter(value.values()))

        return value

    # ---------------------------------------------------------

    def _load_simple_metadata(
        self,
        table: str,
    ) -> list[dict]:

        connection = self.database.open()

        try:

            with connection.cursor() as cursor:

                cursor.execute(
                    f"""
                    SELECT
                        id,
                        name
                    FROM {table}
                    ORDER BY id
                    """
                )

                rows = cursor.fetchall()

                return [
                    {
                        "id": row[0],
                        "name": self._normalize_name(row[1]),
                    }
                    for row in rows
                ]

        finally:

            self.database.close()

    # ---------------------------------------------------------

    def load_companies(self) -> list[dict]:

        return self._load_simple_metadata("res_company")

    # ---------------------------------------------------------

    def load_pos_configs(self) -> list[dict]:

        return self._load_simple_metadata("pos_config")

    # ---------------------------------------------------------

    def load_journals(self) -> list[dict]:

        return self._load_simple_metadata("account_journal")

    # ---------------------------------------------------------

    def load_products(self) -> list[dict]:

        return self._load_simple_metadata("product_template")

    # ---------------------------------------------------------

    def load_partners(self) -> list[dict]:

        return self._load_simple_metadata("res_partner")

    # ---------------------------------------------------------

    def load_warehouses(self) -> list[dict]:

        return self._load_simple_metadata("stock_warehouse")
