import json
from pathlib import Path


class AutoJoin:

    def __init__(self):

        file = Path("database/schema/model_relations.json")

        with open(file, encoding="utf-8") as f:
            self.relations = json.load(f)

    def direct(self, source, target):

        for relation in self.relations:

            if (
                relation["source_table"] == source
                and
                relation["target_table"] == target
            ):

                return relation

        return None

    def join(self, source, target):

        relation = self.direct(source, target)

        if relation is None:

            return None

        return f"""
LEFT JOIN {target}
       ON {target}.{relation['target_field']}
      = {source}.{relation['source_field']}
""".strip()
