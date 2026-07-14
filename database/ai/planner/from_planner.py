"""
FROM Planner

Architecture V9

Builds the FROM clause from a BusinessQuery.
"""

from __future__ import annotations

from database.ai.query.business_query import BusinessQuery


class FromPlanner:
    """
    Builds the FROM clause.
    """

    def build(self, query: BusinessQuery) -> str:

        if not query.entities:
            raise ValueError("No entity found.")

        return query.entities[0]
