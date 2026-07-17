"""
Select Planner

Architecture V9

Builds the SELECT clause from a BusinessQuery.
"""

from __future__ import annotations

from database.ai.query.business_query import BusinessQuery


class SelectPlanner:

    def build(self, query: BusinessQuery) -> list[str]:

        # Aggregate query
        if query.aggregate:

            field = query.field or "*"

            if query.aggregate == "count":
                return [f"COUNT({field})"]

            if query.aggregate == "sum":
                return [f"SUM({field})"]

            if query.aggregate == "avg":
                return [f"AVG({field})"]

            if query.aggregate == "min":
                return [f"MIN({field})"]

            if query.aggregate == "max":
                return [f"MAX({field})"]

        # Standard query
        return ["*"]
