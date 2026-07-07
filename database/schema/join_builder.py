import json


class JoinBuilder:

    def __init__(self):

        with open(
            "database/schema/model_relations.json",
            encoding="utf-8"
        ) as f:

            self.relations = json.load(f)

    def join(self, source, target):

        for r in self.relations:

            if (
                r["source_table"] == source
                and
                r["target_table"] == target
            ):

                return (
                    f"LEFT JOIN {target}\n"
                    f"ON {target}.{r['target_field']} = "
                    f"{source}.{r['source_field']}"
                )

        return None

    def joins_from(self, source):

        joins = []

        for r in self.relations:

            if r["source_table"] == source:

                joins.append(self.join(
                    source,
                    r["target_table"]
                ))

        return joins
