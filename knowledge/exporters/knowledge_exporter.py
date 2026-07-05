import json
from pathlib import Path


class KnowledgeExporter:

    def __init__(self):

        self.output = Path("knowledge/data")

        self.output.mkdir(
            parents=True,
            exist_ok=True
        )

    def export(self, knowledge):

        with open(
            self.output / "knowledge.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                knowledge,
                f,
                indent=4,
                ensure_ascii=False
            )

        print()
        print(f"Saved knowledge for {len(knowledge)} tables")
        print(self.output / "knowledge.json")
