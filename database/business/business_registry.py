"""
Business Registry

Architecture V26
"""

from __future__ import annotations

from database.knowledge.model_dictionary import ModelDictionary


class BusinessRegistry:

    def __init__(
        self,
        models: ModelDictionary | None = None,
    ) -> None:

        self.models = models

        self._registry = {
            "invoice": "account.move",
            "invoices": "account.move",
            "bill": "account.move",
            "bills": "account.move",

            "journal": "account.journal",
            "journals": "account.journal",

            "customer": "res.partner",
            "customers": "res.partner",

            "partner": "res.partner",
            "partners": "res.partner",

            "product": "product.template",
            "products": "product.template",

            "category": "product.category",
            "categories": "product.category",

            "pos": "pos.order",
            "order": "pos.order",
            "orders": "pos.order",
        }

    # ---------------------------------------------------------

    def resolve(self, term: str) -> str | None:

        return self._registry.get(term.lower())

    # ---------------------------------------------------------

    def exists(self, term: str) -> bool:

        return self.resolve(term) is not None
