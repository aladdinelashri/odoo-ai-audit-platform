"""
Model Registry Compatibility Layer

Architecture V60
"""

from __future__ import annotations


class ModelRegistry:

    DEFAULT_MODELS = {
        "invoice": "account.move",
        "customer": "res.partner",
        "partner": "res.partner",
        "product": "product.template",
        "journal": "account.journal",
        "order": "pos.order",
        "pos": "pos.order",
    }

    def __init__(self, registry: dict | None = None):

        self.registry = registry or self.DEFAULT_MODELS.copy()

    def get_model(self, entity: str) -> str | None:

        return self.registry.get(entity)
