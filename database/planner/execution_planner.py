from database.ai.default_fields import DefaultFields
from database.ai.skills.skill_engine import SkillEngine


class ExecutionPlanner:

    def __init__(self):

        self.defaults = DefaultFields()

        self.skills = SkillEngine()

    # ---------------------------------------------------------

    def build(self, parsed):

        entities = parsed["entities"]

        tables = entities["tables"]

        columns = entities["columns"]

        parameters = parsed.get(

            "parameters",

            {}

        )

        # -------------------------------------------------
        # Main Table
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
        # Default Fields
        # -------------------------------------------------

        if not fields:

            if table:

                fields = self.defaults.get(table)

            else:

                fields = ["id"]

        # -------------------------------------------------
        # Order
        # -------------------------------------------------

        order = [

            {

                "field": "date",

                "direction": parameters["order"] or "DESC"

            }

        ]

        # -------------------------------------------------
        # Plan
        # -------------------------------------------------

        plan = {

            "table": table,

            "fields": fields,

            "filters": [],

            "joins": [],

            "order": order,

            "limit": parameters["limit"] or 100

        }

        # -------------------------------------------------
        # Skills
        # -------------------------------------------------

        plan = self.skills.process(

            parsed["text"],

            plan

        )

        # -------------------------------------------------

        return plan
