"""
Value Extractor

Architecture V6

Extracts business values from natural language.
"""

from __future__ import annotations

from database.ai.semantic.value_dictionary import ValueDictionary


class ValueExtractor:

    def __init__(self) -> None:

        self.dictionary = ValueDictionary()

    # ---------------------------------------------------------

    def extract(self, text: str):

        query = text.lower()

        excluded = {
            "today",
            "yesterday",
            "this_month",
            "last_month",
            "this_year",
            "last_year",
        }

        items = sorted(
            self.dictionary.all().items(),
            key=lambda x: len(x[0]),
            reverse=True,
        )

        for keyword, value in items:

            if value in excluded:
                continue

            if keyword in query:
                return value

        return None
