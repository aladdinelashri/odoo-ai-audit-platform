"""
SQL Parameter Compiler

Architecture V34
"""

from __future__ import annotations


class SQLParameterCompiler:

    def compile(self, plan: dict) -> list:

        if plan.get("params"):

            return list(plan["params"])

        if plan.get("where_values"):

            return list(plan["where_values"])

        return []
