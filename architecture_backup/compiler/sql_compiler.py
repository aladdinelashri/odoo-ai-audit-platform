"""
SQL Compiler

Architecture V63
"""

from __future__ import annotations


class SQLCompiler:

    def compile(self, plan: dict) -> str:

        sql = []

        sql.append(
            "SELECT " + ", ".join(plan["select"])
        )

        table = (
            plan.get("from")
            or plan.get("table")
            or plan["model"].replace(".", "_")
        )

        sql.append(
            "FROM " + table
        )

        if plan["where"]:
            sql.append(
                "WHERE " + " AND ".join(plan["where"])
            )

        if plan["order"]:
            sql.append(
                "ORDER BY " + ", ".join(plan["order"])
            )

        if plan["limit"] is not None:
            sql.append(
                f"LIMIT {plan['limit']}"
            )

        return "\n".join(sql)
