import json
from pathlib import Path


class MetadataExporter:

    def __init__(self):

        self.output = Path("data/metadata")

        self.output.mkdir(
            parents=True,
            exist_ok=True
        )

    def export(self, metadata):

        with open(
            self.output / "database.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4,
                ensure_ascii=False
            )

        print()
        print(f"Saved metadata for {len(metadata)} tables")
        print(self.output / "database.json")
