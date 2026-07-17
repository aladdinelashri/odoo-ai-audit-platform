"""
Business Model Dictionary

Architecture V5

Maps business terminology to Odoo models.
"""

from __future__ import annotations


class ModelDictionary:
    """
    Business → Odoo model mapping.
    """

    def __init__(self) -> None:

        self._models = {

            # Accounting
            "invoice": "account.move",
            "invoices": "account.move",
            "bill": "account.move",
            "bills": "account.move",
            "journal entry": "account.move",

            "payment": "account.payment",
            "payments": "account.payment",

            "tax": "account.tax",
            "taxes": "account.tax",

            "account": "account.account",
            "accounts": "account.account",

            "journal": "account.journal",
            "journals": "account.journal",

            # Customers
            "customer": "res.partner",
            "customers": "res.partner",

            "vendor": "res.partner",
            "vendors": "res.partner",

            "supplier": "res.partner",
            "suppliers": "res.partner",

            # Products
            "product": "product.template",
            "products": "product.template",

            "category": "product.category",
            "categories": "product.category",

            # POS
            "order": "pos.order",
            "orders": "pos.order",

            "session": "pos.session",
            "sessions": "pos.session",

            "pos": "pos.order",

            # Inventory
            "stock": "stock.move",
            "inventory": "stock.move",

            # Company
            "company": "res.company",
            "companies": "res.company",

            # Users
            "user": "res.users",
            "users": "res.users",
        }

    # ---------------------------------------------------------

    def resolve(self, word: str) -> str | None:
        """
        Resolve a business word into an Odoo model.
        """

        return self._models.get(word.lower())

    # ---------------------------------------------------------

    def exists(self, word: str) -> bool:
        """
        Returns True if the business word exists.
        """

        return word.lower() in self._models

    # ---------------------------------------------------------

    def all(self) -> dict[str, str]:
        """
        Return the complete dictionary.
        """

        return self._models.copy()
