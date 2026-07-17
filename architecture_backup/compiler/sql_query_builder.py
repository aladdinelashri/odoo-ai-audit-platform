"""
SQL Query Builder

Architecture V62
"""

from __future__ import annotations

from database.compiler.sql_compiler import SQLCompiler
from database.compiler.sql_parameter_compiler import SQLParameterCompiler
from database.metadata.model_registry import ModelRegistry


class SQLQueryBuilder:

    def __init__(
        self,
        model_registry: ModelRegistry | None = None,
    ) -> None:

        self.model_registry = model_registry or ModelRegistry()

        self.sql_compiler = SQLCompiler()
        self.parameter_compiler = SQLParameterCompiler()

    # ---------------------------------------------------------

    @staticmethod
    def _normalize_plan(plan: dict) -> dict:

        plan = dict(plan)

        if not plan.get("table") and plan.get("model"):

            plan["table"] = plan["model"].replace(".", "_")

        elif plan.get("table"):

            plan["table"] = plan["table"].replace(".", "_")

        return plan

    # ---------------------------------------------------------

    def build(self, plan: dict) -> tuple[str, list]:

        plan = self._normalize_plan(plan)

        sql = self.sql_compiler.compile(plan)

        params = self.parameter_compiler.compile(plan)

        return sql, params
