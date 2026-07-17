class JoinBuilder:

    def __init__(self, metadata):

        self.metadata = metadata

    # ---------------------------------------------------------

    def build(self, plan):

        model = plan["model"]

        joins = []

        selected = set(plan["fields"])

        relations = self.metadata.relations_of(model)

        for relation in relations:

            source_field = relation["source_field"]

            target_table = relation["target_table"]

            target_field = relation["target_field"]

            if source_field not in selected:
                continue

            joins.append(

                f"LEFT JOIN {target_table} "
                f"ON {plan['table']}.{source_field} = "
                f"{target_table}.{target_field}"

            )

        plan["joins"] = joins

        return plan
