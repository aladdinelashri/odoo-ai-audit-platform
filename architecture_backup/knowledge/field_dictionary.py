"""
Field Dictionary

Architecture V26
"""

from __future__ import annotations


class FieldDictionary:

    def __init__(self) -> None:
        self._fields = {}

    def add(
        self,
        model: str,
        field: str,
        label: str,
    ) -> None:

        self._fields.setdefault(model, {})

        self._fields[model][field] = {
            "model": model,
            "field": field,
            "label": label,
        }

    def exists(
        self,
        model: str,
        field: str,
    ) -> bool:

        return (
            model in self._fields
            and field in self._fields[model]
        )

    def get(
        self,
        model: str,
        field: str,
    ) -> dict | None:

        return self._fields.get(model, {}).get(field)

    def all(
        self,
        model: str,
    ) -> list[dict]:

        return list(self._fields.get(model, {}).values())
