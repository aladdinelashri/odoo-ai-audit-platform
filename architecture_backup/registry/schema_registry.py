"""
Schema Registry

Architecture V71
"""

from __future__ import annotations

from database.schema.schema_loader import SchemaLoader


class SchemaRegistry:

    def __init__(
        self,
        loader: SchemaLoader | None = None,
    ) -> None:

        self.loader = loader or SchemaLoader()

        self._cache: dict[str, dict] = {}

        self.load()

    # ---------------------------------------------------------

    def load(self) -> None:

        self._cache.clear()

        for table in self.loader.list_tables():

            self._cache[table] = {
                "columns": self.loader.list_columns(table),
                "primary_key": self.loader.primary_key(table),
                "foreign_keys": self.loader.foreign_keys(table),
            }

    # ---------------------------------------------------------

    def has_table(self, table: str) -> bool:

        return table in self._cache

    # ---------------------------------------------------------

    def columns(self, table: str) -> list[str]:

        return self._cache[table]["columns"]

    # ---------------------------------------------------------

    def primary_key(self, table: str):

        return self._cache[table]["primary_key"]

    # ---------------------------------------------------------

    def foreign_keys(self, table: str):

        return self._cache[table]["foreign_keys"]
