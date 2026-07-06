import json
from pathlib import Path
from abc import ABC, abstractmethod


class AuditRule(ABC):

    id = ""

    def metadata(self):

        path = Path(
            "audit/metadata/rules"
        ) / f"{self.id.lower()}.json"

        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @abstractmethod
    def execute(self, executor):
        pass
