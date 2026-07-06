import json
from pathlib import Path


class FrameworkLoader:

    def __init__(self):

        self.path = Path(
            "audit/metadata/frameworks"
        )

    def load(self, framework):

        file = self.path / f"{framework.lower()}.json"

        with open(file, encoding="utf-8") as f:
            return json.load(f)
