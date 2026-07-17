"""
Aggregate Dictionary

Architecture V5

Maps business aggregate words to SQL aggregate functions.
"""

from __future__ import annotations


class AggregateDictionary:
    """
    Business aggregate vocabulary.
    """

    def __init__(self) -> None:

        self._aggregates = {

            "count": "count",
            "number": "count",
            "how many": "count",
            "total count": "count",

            "sum": "sum",
            "total": "sum",

            "average": "avg",
            "avg": "avg",
            "mean": "avg",

            "minimum": "min",
            "minimum value": "min",
            "lowest": "min",
            "smallest": "min",
            "min": "min",

            "maximum": "max",
            "highest": "max",
            "largest": "max",
            "max": "max",
        }

    # ---------------------------------------------------------

    def resolve(self, word: str) -> str | None:

        return self._aggregates.get(word.lower())

    # ---------------------------------------------------------

    def exists(self, word: str) -> bool:

        return word.lower() in self._aggregates

    # ---------------------------------------------------------

    def all(self) -> dict[str, str]:

        return self._aggregates.copy()
