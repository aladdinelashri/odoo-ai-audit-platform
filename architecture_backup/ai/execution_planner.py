from database.ai.default_fields import DefaultFields
from database.ai.join_resolver import JoinResolver


class ExecutionPlanner:

    def __init__(self):

        self.defaults = DefaultFields()

        self.join_resolver = JoinResolver()

    # ---------------------------------------------------------

    def build(self, parsed):

        entities = parsed["entities"]

        parameters = parsed.get("parameters", {})

        models = entities["models"]

        tables = entities["tables"]

        fields_info = entities["fields"]

        # -------------------------------------------------
        # Main Model / Table
        # -------------------------------------------------

        model = models[0] if models else None

        table = tables[0] if tables else None

        # -------------------------------------------------
        # SELECT Fields
        # -------------------------------------------------

        fields = []

        for item in fields_info:

            if item["model"] != model:
                continue

            field = item["field"]

            if field not in fields:

                fields.append(field)

        # -------------------------------------------------
        # Default Fields
        # -------------------------------------------------

        if not fields:

            if table:

                fields = self.defaults.get(table)

            else:

                fields = ["id"]

        # -------------------------------------------------
        # JOINS
        # -------------------------------------------------

        joins = self.join_resolver.resolve(

            model,

            fields_info

        )

        # -------------------------------------------------
        # Parameters
        # -------------------------------------------------

        limit = parameters.get("limit", 100)

        direction = parameters.get("order", "DESC")

        # -------------------------------------------------

        plan = {

            "success": True,

            "model": model,

            "table": table,

            "fields": fields,

            "filters": [],

            "joins": joins,

            "group_by": [],

            "order_by": [

                {

                    "field": "date",

                    "direction": direction

                }

            ],

            "aggregate": None,

            "limit": limit

        }

        return plan
