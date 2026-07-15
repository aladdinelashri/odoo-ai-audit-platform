"""
SQL Query Builder

Architecture V22
"""

from __future__ import annotations

from database.compiler.sql_compiler import SQLCompiler
from database.compiler.sql_parameter_compiler import SQLParameterCompiler


class SQLQueryBuilder:

    def __init__(self) -> None:

        self.sql_compiler = SQLCompiler()
        self.parameter_compiler = SQLParameterCompiler()

    # ---------------------------------------------------------

    @staticmethod
    def _normalize_table(plan: dict) -> dict:

        plan = dict(plan)

        if "table" in plan and plan["table"]:

            # Odoo model -> PostgreSQL table
            plan["table"] = plan["table"].replace(".", "_")

        return plan

    # ---------------------------------------------------------

    def build(self, plan: dict) -> tuple[str, list]:

        plan = self._normalize_table(plan)

        sql = self.sql_compiler.compile(plan)

        params = self.parameter_compiler.compile(plan)

        return sql, params
