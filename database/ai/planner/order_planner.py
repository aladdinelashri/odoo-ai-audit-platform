"""
ORDER BY Planner

Architecture V9

Builds the ORDER BY clause from a BusinessQuery.
"""

from __future__ import annotations

from database.ai.query.business_query import BusinessQuery


class OrderPlanner:

    def build(self, query: BusinessQuery) -> list[str]:

        if query.metadata.get("order_by"):

            direction = query.metadata.get("direction", "ASC")

            return [
                f"{query.metadata['order_by']} {direction}"
            ]

        return []
