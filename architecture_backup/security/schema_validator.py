"""
Schema Validator

Architecture V20
"""

from __future__ import annotations

from database.services.metadata_service import MetadataService


class SchemaValidator:

    def __init__(self, metadata: MetadataService):

        self.metadata = metadata

    # ---------------------------------------------------------

    def table_exists(self, model: str) -> bool:

        return self.metadata.has_model(model)

    # ---------------------------------------------------------

    def column_exists(
        self,
        model: str,
        column: str,
    ) -> bool:

        if not self.metadata.has_model(model):
            return False

        return column in self.metadata.columns(model)
