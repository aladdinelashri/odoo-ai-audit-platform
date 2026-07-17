"""
Model Dictionary

Architecture V26
"""

from __future__ import annotations


class ModelDictionary:

    def __init__(self) -> None:
        self._models = {}

    def add(
        self,
        model: str,
        display_name: str,
    ) -> None:

        self._models[model] = {
            "model": model,
            "display_name": display_name,
        }

    def exists(self, model: str) -> bool:

        return model in self._models

    def get(self, model: str) -> dict | None:

        return self._models.get(model)

    def all(self) -> list[dict]:

        return list(self._models.values())
