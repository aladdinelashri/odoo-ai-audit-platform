"""
SQL Parameter Compiler

Architecture V10

Extracts SQL parameters from a logical SQL plan.
"""

from __future__ import annotations


class SQLParameterCompiler:

    def compile(self, plan: dict) -> list:

        params: list = []

        if plan.get("where_values"):

            params.extend(plan["where_values"])

        return params
