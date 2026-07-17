"""
Core SQL Builder

Architecture V3

Converts an execution plan into a PostgreSQL SQL statement.
"""

from __future__ import annotations

from database.core.pipeline.context import PipelineContext


class SQLBuilder:
    """
    Architecture V3 SQL Builder.
    """

    # ---------------------------------------------------------

    def build(self, context: PipelineContext) -> str:

        plan = context.execution_plan

        if not plan or not plan.get("success"):

            raise ValueError("Invalid execution plan.")

        sql = []

        aggregate = plan.get("aggregate")

        # ---------------------------------------------------------
        # SELECT
        # ---------------------------------------------------------

        if aggregate:

            function = aggregate["function"].upper()

            field = aggregate["field"]

            sql.append(f"SELECT {function}({field})")

        else:

            sql.append(

                "SELECT " + ", ".join(plan["fields"])

            )

        # ---------------------------------------------------------
        # FROM
        # ---------------------------------------------------------

        sql.append(f"FROM {plan['table']}")

        # ---------------------------------------------------------
        # JOINS
        # ---------------------------------------------------------

        for join in plan.get("joins", []):

            sql.append(join)

        # ---------------------------------------------------------
        # WHERE
        # ---------------------------------------------------------

        filters = plan.get("filters", [])

        if filters:

            where = []

            for item in filters:

                value = item["value"]

                if isinstance(value, str):

                    value = f"'{value}'"

                elif value is None:

                    value = "NULL"

                where.append(

                    f"{item['field']} {item['operator']} {value}"

                )

            sql.append("WHERE " + " AND ".join(where))

        # ---------------------------------------------------------
        # GROUP BY
        # ---------------------------------------------------------

        if not aggregate and plan.get("group_by"):

            sql.append(

                "GROUP BY " + ", ".join(plan["group_by"])

            )

        # ---------------------------------------------------------
        # ORDER BY
        # ---------------------------------------------------------

        if not aggregate and plan.get("order_by"):

            order = []

            for item in plan["order_by"]:

                order.append(

                    f"{item['field']} {item.get('direction','ASC')}"

                )

            sql.append("ORDER BY " + ", ".join(order))

        # ---------------------------------------------------------
        # LIMIT
        # ---------------------------------------------------------

        if not aggregate and plan.get("limit"):

            sql.append(f"LIMIT {plan['limit']}")

        context.sql = "\n".join(sql)

        return context.sql
