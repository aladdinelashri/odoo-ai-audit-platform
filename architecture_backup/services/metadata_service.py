"""
Metadata Service

Architecture V18
"""

from __future__ import annotations

from database.odoo.model_registry import ModelRegistry
from database.registry.schema_registry import SchemaRegistry


class MetadataService:

    def __init__(
        self,
        schema_registry: SchemaRegistry,
        model_registry: ModelRegistry,
    ) -> None:

        self.schema = schema_registry
        self.models = model_registry

    # ---------------------------------------------------------

    def has_model(self, model: str) -> bool:

        return self.models.has_model(model)

    # ---------------------------------------------------------

    def table(self, model: str) -> str:

        return self.models.table(model)

    # ---------------------------------------------------------

    def columns(self, model: str) -> list[str]:

        table = self.table(model)

        return self.schema.columns(table)

    # ---------------------------------------------------------

    def primary_key(self, model: str):

        table = self.table(model)

        return self.schema.primary_key(table)

    # ---------------------------------------------------------

    def foreign_keys(self, model: str):

        table = self.table(model)

        return self.schema.foreign_keys(table)
