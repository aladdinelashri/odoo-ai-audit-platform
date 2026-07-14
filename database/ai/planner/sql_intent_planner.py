"""
SQL Intent Planner

Architecture V13

Converts a BusinessQuery into a SQL execution plan.
"""

from __future__ import annotations

from database.ai.query.business_query import BusinessQuery


class SQLIntentPlanner:

    def build(self, query: BusinessQuery) -> dict:

        if not query.entities:
            raise ValueError("No business entity found.")

        table = query.entities[0]

        # -------------------------
        # SELECT
        # -------------------------

        if query.aggregate:

            if query.field:
                select = [f"{query.aggregate}({query.field})"]
            else:
                select = [f"{query.aggregate}(*)"]

            limit = None

        else:

            select = ["*"]
            limit = 100

        # -------------------------
        # WHERE
        # -------------------------

        where = []
        where_values = []

        if query.operator and query.value is not None:

            field = query.field or "state"

            where.append(f"{field} {query.operator} %s")
            where_values.append(query.value)

        # -------------------------
        # ORDER
        # -------------------------

        order = []

        return {
            "select": select,
            "from": table,
            "where": where,
            "where_values": where_values,
            "order": order,
            "limit": limit,
        }
