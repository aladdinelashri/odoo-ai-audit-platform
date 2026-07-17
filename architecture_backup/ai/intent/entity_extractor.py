"""
Entity Extractor

Architecture V6

Extracts business entities from natural language.
"""

from __future__ import annotations

from database.ai.semantic.model_dictionary import ModelDictionary


class EntityExtractor:

    def __init__(self) -> None:

        self.dictionary = ModelDictionary()

    # ---------------------------------------------------------

    def extract(self, text: str) -> list[str]:

        query = text.lower()

        entities: list[str] = []

        for word, model in self.dictionary.all().items():

            if word in query and model not in entities:

                entities.append(model)

        return entities
