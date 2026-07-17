"""
Business Field Dictionary

Architecture V5

Maps business field names to Odoo fields.
"""

from __future__ import annotations


class FieldDictionary:
    """
    Business field vocabulary.
    """

    def __init__(self) -> None:

        self._fields = {

            # Invoice
            "invoice": "name",
            "number": "name",

            # Dates
            "date": "invoice_date",
            "invoice date": "invoice_date",
            "due date": "invoice_date_due",

            # Money
            "amount": "amount_total",
            "total": "amount_total",
            "total amount": "amount_total",
            "untaxed": "amount_untaxed",
            "tax": "amount_tax",
            "residual": "amount_residual",

            # Partner
            "customer": "partner_id",
            "vendor": "partner_id",
            "partner": "partner_id",

            # Product
            "product": "product_id",

            # Quantity
            "quantity": "quantity",

            # Price
            "price": "price_unit",

            # State
            "status": "state",
            "state": "state",

            # Company
            "company": "company_id",

            # Journal
            "journal": "journal_id",
        }

    # ---------------------------------------------------------

    def resolve(self, word: str) -> str | None:
        return self._fields.get(word.lower())

    # ---------------------------------------------------------

    def exists(self, word: str) -> bool:
        return word.lower() in self._fields

    # ---------------------------------------------------------

    def all(self) -> dict[str, str]:
        return self._fields.copy()
