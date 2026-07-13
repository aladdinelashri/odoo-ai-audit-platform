from database.odoo.semantic_registry import SemanticRegistry


class DefaultFieldSelector:

    def __init__(self):

        self.semantic = SemanticRegistry()

    # ---------------------------------------------------------

    def select(self, model):

        fields = self.semantic.model(model)

        if not fields:
            return ["id"]

        priority = [

            "display_name",
            "date",
            "business_partner",
            "customer",
            "vendor",
            "product",
            "monetary",
            "price",
            "total",
            "quantity",
            "status"

        ]

        selected = []

        for role in priority:

            for field, info in fields.items():

                if info["semantic_role"] == role:

                    if field not in selected:

                        selected.append(field)

        if not selected:

            selected.append("id")

        return selected
