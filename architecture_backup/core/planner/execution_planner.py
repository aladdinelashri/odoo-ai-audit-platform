"""
Core Execution Planner

Architecture V3

Transforms the normalized parsed query into an executable plan.
"""

from __future__ import annotations

from database.core.pipeline.context import PipelineContext

from database.ai.default_fields import DefaultFields
from database.ai.join_resolver import JoinResolver


class ExecutionPlanner:
    """
    Architecture V3 Execution Planner.
    """

    def __init__(self) -> None:

        self.default_fields = DefaultFields()

        self.join_resolver = JoinResolver()

    # ------------------------------------------------------------------

    def build(self, context: PipelineContext) -> dict:

        parsed = context.parsed

        entities = parsed["entities"]

        parameters = parsed.get("parameters", {})

        aggregate = parsed.get("aggregate")

        filters = parsed.get("filters", [])

        tables = entities.get("tables", [])

        fields_info = entities.get("fields", [])

        # ------------------------------------------------------------
        # Main Table
        # ------------------------------------------------------------

        table = tables[0] if tables else None

        # ------------------------------------------------------------
        # Selected Fields
        # ------------------------------------------------------------

        fields = []

        for item in fields_info:

            field = item["field"]

            if field not in fields:

                fields.append(field)

        if not fields:

            fields = self.default_fields.get(table)

        # ------------------------------------------------------------
        # Aggregate
        # ------------------------------------------------------------

        aggregate_plan = None

        if aggregate:

            if aggregate.upper() == "COUNT":

                aggregate_field = "id"

            else:

                numeric_candidates = [

                    "amount_total",

                    "balance",

                    "debit",

                    "credit",

                    "price_total",

                    "price_subtotal",

                    "quantity",

                ]

                aggregate_field = None

                for field in numeric_candidates:

                    if field in fields:

                        aggregate_field = field

                        break

                if aggregate_field is None:

                    aggregate_field = "amount_total"

            aggregate_plan = {

                "function": aggregate,

                "field": aggregate_field,

            }

        # ------------------------------------------------------------
        # Joins
        # ------------------------------------------------------------

        joins = []

        if table:

            joins = self.join_resolver.resolve(

                entities["models"][0],

                fields_info,

            )

        # ------------------------------------------------------------
        # Execution Plan
        # ------------------------------------------------------------

        plan = {

            "success": True,

            "table": table,

            "fields": fields,

            "filters": filters,

            "joins": joins,

            "group_by": [],

            "order_by": [

                {

                    "field": "date",

                    "direction": parameters.get(

                        "order",

                        "DESC",

                    ),

                }

            ],

            "aggregate": aggregate_plan,

            "limit": parameters.get(

                "limit",

                100,

            ),

        }

        context.execution_plan = plan

        return plan
