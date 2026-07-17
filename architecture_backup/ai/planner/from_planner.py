"""
FROM Planner

Architecture V22
"""

from __future__ import annotations

from database.ai.query.business_query import BusinessQuery


class FromPlanner:
    """
    Builds the SQL FROM clause.
    Converts an Odoo model name into a PostgreSQL table name.
    """

    def build(self, query: BusinessQuery) -> str:

        if not query.entities:
            raise ValueError("No entity found.")

        model = query.entities[0]

        # Odoo model -> PostgreSQL table
        return model.replace(".", "_")
