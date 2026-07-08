from database.ai.default_fields import DefaultFields


class ExecutionPlanner:

    def __init__(self):

        self.defaults = DefaultFields()

    # ---------------------------------------------------------

    def build(self, parsed):

        entities = parsed["entities"]

        parameters = parsed.get("parameters", {})

        tables = entities["tables"]

        columns = entities["columns"]

        # -------------------------------------------------
        # Main table
        # -------------------------------------------------

        table = tables[0] if tables else None

        # -------------------------------------------------
        # Fields
        # -------------------------------------------------

        fields = []

        for column in columns:

            name = column["name"]

            if table:

                if table in column["tables"]:

                    fields.append(name)

            else:

                fields.append(name)

        # -------------------------------------------------
        # Default fields
        # -------------------------------------------------

        if not fields:

            if table:

                fields = self.defaults.get(table)

            else:

                fields = ["id"]

        # -------------------------------------------------
        # Parameters
        # -------------------------------------------------

        limit = parameters.get("limit", 100)

        direction = parameters.get("order", "DESC")

        # -------------------------------------------------

        plan = {

            "table": table,

            "fields": fields,

            "filters": [],

            "joins": [],

            "order": [

                {

                    "field": "date",

                    "direction": direction

                }

            ],

            "limit": limit

        }

        return plan
