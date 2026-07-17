"""
LIMIT Planner

Architecture V9

Builds the LIMIT clause from a BusinessQuery.
"""

from __future__ import annotations

from database.ai.query.business_query import BusinessQuery


class LimitPlanner:

    DEFAULT_LIMIT = 100

    def build(self, query: BusinessQuery) -> int | None:

        if query.metadata.get("limit") is not None:
            return int(query.metadata["limit"])

        if query.aggregate:
            return None

        return self.DEFAULT_LIMIT
