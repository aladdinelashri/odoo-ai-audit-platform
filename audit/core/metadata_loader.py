import json
from pathlib import Path


class MetadataLoader:

    ROOT = Path("audit/metadata")

    @classmethod
    def load_rule(cls, rule_id: str):

        path = cls.ROOT / "rules" / f"{rule_id.lower()}.json"

        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def load_framework(cls, framework: str):

        path = cls.ROOT / "frameworks" / f"{framework.lower()}.json"

        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def load_json(cls, relative_path: str):

        path = cls.ROOT / relative_path

        with open(path, encoding="utf-8") as f:
            return json.load(f)
