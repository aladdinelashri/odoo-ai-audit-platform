"""
Odoo Model Registry

Architecture V17
"""

from __future__ import annotations

from database.registry.schema_registry import SchemaRegistry


class ModelRegistry:

    def __init__(self, registry: SchemaRegistry):

        self.registry = registry

        self._models: dict[str, str] = {}

    # ---------------------------------------------------------

    @staticmethod
    def table_to_model(table: str) -> str:

        return table.replace("_", ".")

    # ---------------------------------------------------------

    @staticmethod
    def model_to_table(model: str) -> str:

        return model.replace(".", "_")

    # ---------------------------------------------------------

    def build(self) -> None:

        self._models.clear()

        for table in self.registry._cache.keys():

            model = self.table_to_model(table)

            self._models[model] = table

    # ---------------------------------------------------------

    def has_model(self, model: str) -> bool:

        return model in self._models

    # ---------------------------------------------------------

    def table(self, model: str) -> str:

        return self._models[model]
