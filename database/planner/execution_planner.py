from database.ai.ai_context import AIContext
from database.ai.aggregate_resolver import AggregateResolver
from database.ai.entity_detector import EntityDetector
from database.ai.filter_field_resolver import FilterFieldResolver
from database.ai.intent_detector import IntentDetector
from database.ai.parameter_resolver import ParameterResolver
from database.odoo.database_field_resolver import DatabaseFieldResolver


class ExecutionPlanner:

    def __init__(self):

        self.context = AIContext()

        self.entities = EntityDetector()

        self.intent = IntentDetector()

        self.parameters = ParameterResolver()

        self.aggregate = AggregateResolver()

        self.database_fields = DatabaseFieldResolver()

        self.filter_fields = FilterFieldResolver()

    # ---------------------------------------------------------

    def build(self, text):

        self.context.initialize()

        entity_result = self.entities.detect(text)

        intent = self.intent.detect(text)

        params = self.parameters.resolve(text)

        models = entity_result["models"]

        detected_fields = entity_result["fields"]

        if not models:

            return {

                "success": False,

                "reason": "no_model_detected"

            }

        model = models[0]

        table = self.context.table(model)

        # -------------------------------------------------
        # Explicit fields
        # -------------------------------------------------

        explicit_fields = []

        for item in detected_fields:

            if item["model"] != model:

                continue

            field = self.database_fields.resolve(

                model,

                item["field"]

            )

            explicit_fields.append(field)

        # -------------------------------------------------
        # Selected fields
        # -------------------------------------------------

        if explicit_fields:

            selected_fields = explicit_fields

        else:

            selected_fields = [

                self.database_fields.resolve(model, field)

                for field in self.context.default_fields(model)

            ]

        # -------------------------------------------------
        # Resolve filter fields
        # -------------------------------------------------

        filters = self.filter_fields.resolve(

            model=model,

            detected_fields=selected_fields,

            filters=params["filters"]

        )

        # -------------------------------------------------
        # Build Plan
        # -------------------------------------------------

        plan = {

            "success": True,

            "intent": intent.name,

            "model": model,

            "table": table,

            "fields": selected_fields,

            "filters": filters,

            "joins": [],

            "group_by": [],

            "order_by": [],

            "aggregate": None,

            "limit": params["limit"] or 100

        }

        # -------------------------------------------------
        # Order
        # -------------------------------------------------

        if params["order"]:

            plan["order_by"].append(

                {

                    "field": "date",

                    "direction": params["order"]

                }

            )

        # -------------------------------------------------
        # Aggregate
        # -------------------------------------------------

        if intent.name in (

            "count",

            "sum",

            "average",

            "max",

            "min"

        ):

            aggregate_field = self.aggregate.resolve(

                intent=intent.name,

                default_fields=selected_fields,

                detected_fields=explicit_fields

            )

            aggregate_field = self.database_fields.resolve(

                model,

                aggregate_field

            )

            if intent.name == "count":

                aggregate_field = "id"

            plan["aggregate"] = {

                "function": intent.name,

                "field": aggregate_field

            }

        return plan
