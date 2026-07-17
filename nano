"""
Value Dictionary

Architecture V5

Maps business values into normalized internal values.
"""

from __future__ import annotations


class ValueDictionary:
    """
    Business value vocabulary.
    """

    def __init__(self) -> None:

        self._values = {

            # Invoice states
            "paid": "posted",
            "open": "posted",
            "draft": "draft",
            "cancelled": "cancel",
            "canceled": "cancel",

            # Partner types
            "customer": "customer",
            "vendor": "supplier",
            "supplier": "supplier",

            # Dates
            "today": "today",
            "yesterday": "yesterday",
            "this month": "this_month",
            "last month": "last_month",
            "this year": "this_year",
            "last year": "last_year",

            # Boolean
            "true": True,
            "false": False,
            "yes": True,
            "no": False,
        }

    # ---------------------------------------------------------

    def resolve(self, value: str):

        return self._values.get(value.lower())

    # ---------------------------------------------------------

    def exists(self, value: str) -> bool:

        return value.lower() in self._values

    # ---------------------------------------------------------

    def all(self):

        return self._values.copy()
