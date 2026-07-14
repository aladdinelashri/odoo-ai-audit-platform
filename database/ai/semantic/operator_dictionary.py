"""
Operator Dictionary

Architecture V5

Maps business comparison operators to SQL operators.
"""

from __future__ import annotations


class OperatorDictionary:
    """
    Business operator vocabulary.
    """

    def __init__(self) -> None:

        self._operators = {

            # Equality
            "equals": "=",
            "equal": "=",
            "is": "=",
            "=": "=",

            # Not equal
            "not equal": "!=",
            "!=": "!=",

            # Greater
            "greater": ">",
            "greater than": ">",
            ">": ">",

            # Less
            "less": "<",
            "less than": "<",
            "<": "<",

            # Greater or equal
            "greater or equal": ">=",
            "greater than or equal": ">=",
            ">=": ">=",

            # Less or equal
            "less or equal": "<=",
            "less than or equal": "<=",
            "<=": "<=",

            # Range
            "between": "BETWEEN",

            # Text
            "contains": "ILIKE",
            "starts with": "ILIKE",
            "ends with": "ILIKE",

            # Dates
            "before": "<",
            "after": ">",

        }

    # ---------------------------------------------------------

    def resolve(self, word: str) -> str | None:

        return self._operators.get(word.lower())

    # ---------------------------------------------------------

    def exists(self, word: str) -> bool:

        return word.lower() in self._operators

    # ---------------------------------------------------------

    def all(self) -> dict[str, str]:

        return self._operators.copy()
