"""
V4 Metadata Loader

Loads metadata exported by the existing metadata builder.

Source:
database/metadata/*.json
"""

from __future__ import annotations

import json
from pathlib import Path

from database.v4.metadata.metadata_cache import MetadataCache
from database.v4.metadata.metadata_models import MetadataModel
from database.v4.metadata.metadata_fields import MetadataField


class MetadataLoader:

    def __init__(self):

        self.cache = MetadataCache()

        self.metadata_path = (
            Path(__file__).resolve().parents[2]
            / "metadata"
        )

    # ---------------------------------------------------------

    def load(self):

        if self.cache.has("models"):

            return self.cache.get("models")

        models = {}

        for file in self.metadata_path.glob("*.json"):

            if file.name == "models.json":
                continue

            with open(file, "r", encoding="utf-8") as f:

                data = json.load(f)

            model_name = data.get("model")

            if not model_name:
                continue

            table_name = data.get(
                "table",
                model_name.replace(".", "_")
            )

            model = MetadataModel(

                model=model_name,

                table=table_name,

                label=model_name,

            )

            fields = data.get("fields", [])

            # -------------------------------------------------
            # Old metadata format
            # -------------------------------------------------

            if isinstance(fields, dict):

                for field_name, info in fields.items():

                    field = MetadataField(

                        model=model_name,

                        table=table_name,

                        name=field_name,

                        label=info.get(
                            "label",
                            field_name
                        ),

                        data_type=info.get(
                            "type",
                            "unknown"
                        ),

                        relation=info.get(
                            "relation"
                        ),

                    )

                    model.add_field(field)

            # -------------------------------------------------
            # Excel metadata format
            # -------------------------------------------------

            elif isinstance(fields, list):

                for info in fields:

                    field_name = info["name"]

                    field = MetadataField(

                        model=model_name,

                        table=table_name,

                        name=field_name,

                        label=field_name,

                        data_type=info.get(
                            "type",
                            "unknown"
                        ),

                        relation=None,

                    )

                    model.add_field(field)

            models[model_name] = model

        self.cache.set(

            "models",

            models,

        )

        return models
