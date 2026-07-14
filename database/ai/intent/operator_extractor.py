"""
Operator Extractor

Architecture V6

Extracts comparison operators from natural language.
"""

from __future__ import annotations

from database.ai.semantic.operator_dictionary import OperatorDictionary


class OperatorExtractor:

    def __init__(self) -> None:

        self.dictionary = OperatorDictionary()

    # ---------------------------------------------------------

    def extract(self, text: str) -> str | None:

        query = text.lower()

        # Longest phrases first
        items = sorted(
            self.dictionary.all().items(),
            key=lambda x: len(x[0]),
            reverse=True,
        )

        for keyword, operator in items:

            if keyword in query:

                return operator

        return None
