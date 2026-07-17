"""
Field Registry

Architecture V70
"""

from __future__ import annotations

import json
from pathlib import Path


class FieldRegistry:

    def __init__(self) -> None:

        self.schema_path = (
            Path(__file__).resolve().parents[1]
            / "schema"
        )

        self.cache: dict[str, dict] = {}

    # ---------------------------------------------------------

    def reload(self) -> None:

        self.cache.clear()

    # ---------------------------------------------------------

    def _load_model(self, model: str) -> dict:

        if model in self.cache:
            return self.cache[model]

        file = self.schema_path / f"{model}.json"

        if not file.exists():
            self.cache[model] = {"fields": []}
            return self.cache[model]

        with open(file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        self.cache[model] = metadata

        return metadata

    # ---------------------------------------------------------

    def models(self) -> list[str]:

        models = []

        for file in self.schema_path.glob("*.json"):

            if "." in file.stem:
                models.append(file.stem)

        return sorted(models)

    # ---------------------------------------------------------

    def get_fields(self, model: str) -> list[str]:

        metadata = self._load_model(model)

        return [
            field["name"]
            for field in metadata.get("fields", [])
        ]

    # ---------------------------------------------------------

    def get_relation(
        self,
        model: str,
        field_name: str,
    ) -> str | None:

        metadata = self._load_model(model)

        for field in metadata.get("fields", []):

            if field["name"] == field_name:
                return field.get("relation")

        return None

    # ---------------------------------------------------------

    def get_type(
        self,
        model: str,
        field_name: str,
    ) -> str | None:

        metadata = self._load_model(model)

        for field in metadata.get("fields", []):

            if field["name"] == field_name:
                return field.get("type")

        return None

    # ---------------------------------------------------------

    def exists(
        self,
        model: str,
        field_name: str,
    ) -> bool:

        return field_name in self.get_fields(model)
