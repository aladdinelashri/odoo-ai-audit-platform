"""
Where Planner

Architecture V9

Builds the WHERE clause from a BusinessQuery.
"""

from __future__ import annotations

from database.ai.query.business_query import BusinessQuery


class WherePlanner:

    def build(self, query: BusinessQuery) -> list[str]:

        conditions: list[str] = []

        if (
            query.field
            and query.operator
            and query.value is not None
        ):
            conditions.append(
                f"{query.field} {query.operator} %s"
            )

        if query.date == "today":
            conditions.append(
                "DATE(create_date)=CURRENT_DATE"
            )

        elif query.date == "yesterday":
            conditions.append(
                "DATE(create_date)=CURRENT_DATE - INTERVAL '1 day'"
            )

        elif query.date == "this_month":
            conditions.append(
                "DATE_TRUNC('month', create_date)=DATE_TRUNC('month', CURRENT_DATE)"
            )

        elif query.date == "last_month":
            conditions.append(
                "DATE_TRUNC('month', create_date)=DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')"
            )

        elif query.date == "this_year":
            conditions.append(
                "DATE_TRUNC('year', create_date)=DATE_TRUNC('year', CURRENT_DATE)"
            )

        elif query.date == "last_year":
            conditions.append(
                "DATE_TRUNC('year', create_date)=DATE_TRUNC('year', CURRENT_DATE - INTERVAL '1 year')"
            )

        return conditions
