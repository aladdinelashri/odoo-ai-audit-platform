import json
from pathlib import Path


class MetadataLoader:

    def load_json(self, path):
        file = Path(path)

        if not file.exists():
            return {}

        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
