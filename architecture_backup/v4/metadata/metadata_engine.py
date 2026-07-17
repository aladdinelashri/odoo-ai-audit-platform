"""
V4 Metadata Engine

Production Architecture

Single source of truth for all metadata access.
"""

from __future__ import annotations

from database.v4.metadata.metadata_loader import MetadataLoader


class MetadataEngine:

    def __init__(self):

        self.loader = MetadataLoader()

        self.models = self.loader.load()

    # ---------------------------------------------------------

    def all_models(self):

        return self.models

    # ---------------------------------------------------------

    def model(self, model_name: str):

        return self.models.get(model_name)

    # ---------------------------------------------------------

    def exists(self, model_name: str):

        return model_name in self.models

    # ---------------------------------------------------------

    def table(self, model_name: str):

        model = self.model(model_name)

        if not model:

            return None

        return model.table

    # ---------------------------------------------------------

    def fields(self, model_name: str):

        model = self.model(model_name)

        if not model:

            return []

        return model.fields

    # ---------------------------------------------------------

    def relations(self, model_name: str):

        model = self.model(model_name)

        if not model:

            return []

        return model.relations

    # ---------------------------------------------------------

    def statistics(self, model_name: str):

        model = self.model(model_name)

        if not model:

            return None

        return model.statistics
