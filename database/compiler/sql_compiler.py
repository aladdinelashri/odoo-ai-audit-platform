"""
SQL Compiler

Architecture V10

Compiles a logical SQL plan into executable SQL.
"""

from __future__ import annotations


class SQLCompiler:

    def compile(self, plan: dict) -> str:

        sql = []

        # SELECT
        sql.append(
            "SELECT " + ", ".join(plan["select"])
        )

        # FROM
        sql.append(
            "FROM " + plan["from"]
        )

        # WHERE
        if plan["where"]:
            sql.append(
                "WHERE " + " AND ".join(plan["where"])
            )

        # ORDER BY
        if plan["order"]:
            sql.append(
                "ORDER BY " + ", ".join(plan["order"])
            )

        # LIMIT
        if plan["limit"] is not None:
            sql.append(
                f"LIMIT {plan['limit']}"
            )

        return "\n".join(sql)
