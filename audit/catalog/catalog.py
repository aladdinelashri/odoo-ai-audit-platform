from pathlib import Path
import json


class AuditCatalog:

    def __init__(self):

        self.path = Path(
            "audit/metadata/rules"
        )

    def load(self):

        rules = []

        for file in sorted(self.path.glob("*.json")):

            with open(file, encoding="utf-8") as f:
                rules.append(json.load(f))

        return rules

    def count(self):

        return len(self.load())
