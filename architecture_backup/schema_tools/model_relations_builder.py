import json
from pathlib import Path


class ModelRelationsBuilder:

    ID_SUFFIX = "_id"

    def __init__(self):

        self.schema_file = Path("database/schema/schema.json")
        self.output_file = Path("database/schema/model_relations.json")

        with open(self.schema_file, encoding="utf-8") as f:
            self.schema = json.load(f)

        self.tables = set(self.schema.keys())

    def guess_table(self, field):

        if not field.endswith(self.ID_SUFFIX):
            return None

        base = field[:-3]

        candidates = [

            base,
            f"res_{base}",
            f"account_{base}",
            f"stock_{base}",
            f"product_{base}",
            f"pos_{base}",
            f"sale_{base}",
            f"purchase_{base}",
            f"hr_{base}",
            f"mrp_{base}",

        ]

        for table in candidates:

            if table in self.tables:
                return table

        return None

    def build(self):

        relations = []

        for table, columns in self.schema.items():

            for column in columns:

                field = column["column_name"]

                if not field.endswith("_id"):
                    continue

                target = self.guess_table(field)

                if not target:
                    continue

                relations.append({

                    "source_table": table,
                    "source_field": field,
                    "target_table": target,
                    "target_field": "id"

                })

        with open(
            self.output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                relations,
                f,
                indent=4,
                ensure_ascii=False
            )

        print()

        print("=" * 70)
        print("Model Relations")
        print("=" * 70)

        print()

        print(f"Relations : {len(relations)}")

        print()

        print(f"Saved to {self.output_file}")

        return relations


if __name__ == "__main__":

    ModelRelationsBuilder().build()
