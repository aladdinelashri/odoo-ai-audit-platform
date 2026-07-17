"""
Date Extractor

Architecture V6

Extracts business date expressions from natural language.
"""

from __future__ import annotations


class DateExtractor:

    def __init__(self) -> None:

        self._dates = {
            "this month": "this_month",
            "last month": "last_month",
            "this year": "this_year",
            "last year": "last_year",
            "yesterday": "yesterday",
            "today": "today",
        }

    # ---------------------------------------------------------

    def extract(self, text: str) -> str | None:

        query = text.lower()

        for phrase, value in sorted(
            self._dates.items(),
            key=lambda x: len(x[0]),
            reverse=True,
        ):
            if phrase in query:
                return value

        return None
