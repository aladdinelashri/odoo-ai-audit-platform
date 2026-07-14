"""
Aggregate Extractor

Architecture V6

Extracts aggregate operations from natural language.
"""

from __future__ import annotations

from database.ai.semantic.aggregate_dictionary import AggregateDictionary


class AggregateExtractor:

    def __init__(self) -> None:

        self.dictionary = AggregateDictionary()

    # ---------------------------------------------------------

    def extract(self, text: str) -> str | None:

        query = text.lower()

        for keyword, aggregate in self.dictionary.all().items():

            if keyword in query:

                return aggregate

        return None
