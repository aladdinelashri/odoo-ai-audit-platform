from database.ai.ai_context import AIContext


class JoinResolver:

    def __init__(self):

        self.context = AIContext()

    # ---------------------------------------------------------

    def resolve(self, model, detected_fields):

        self.context.initialize()

        joins = []

        seen = set()

        metadata = self.context.metadata.all_models().get(model)

        if not metadata:

            return joins

        fields = metadata.get("fields", {})

        source_table = self.context.table(model)

        for item in detected_fields:

            if item["model"] != model:

                continue

            field_name = item["field"]

            field = fields.get(field_name)

            if not field:

                continue

            relation = field.get("relation")

            if not relation:

                continue

            target_table = self.context.table(relation)

            if not target_table:

                continue

            sql = (

                f"LEFT JOIN {target_table} "

                f"ON {target_table}.id = {source_table}.{field_name}"

            )

            if sql not in seen:

                seen.add(sql)

                joins.append(sql)

        return joins
