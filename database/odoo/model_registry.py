"""
Odoo Model Registry

Architecture V72
"""

from __future__ import annotations

from database.registry.schema_registry import SchemaRegistry


class ModelRegistry:

    def __init__(
        self,
        registry: SchemaRegistry | None = None,
    ) -> None:

        self.registry = registry or SchemaRegistry()

        self._models: dict[str, str] = {}

        self.build()

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

        for table in self.registry._cache:

            self._models[self.table_to_model(table)] = table

    # ---------------------------------------------------------

    def models(self) -> list[str]:

        return sorted(self._models.keys())

    # ---------------------------------------------------------

    def has_model(self, model: str) -> bool:

        return model in self._models

    # ---------------------------------------------------------

    def table(self, model: str) -> str:

        return self._models[model]

    # ---------------------------------------------------------

    def get_model(self, alias: str) -> str | None:

        aliases = {
            "invoice": "account.move",
            "customer": "res.partner",
            "partner": "res.partner",
            "journal": "account.journal",
            "product": "product.template",
            "order": "pos.order",
            "pos": "pos.order",
        }

        return aliases.get(alias, alias)
