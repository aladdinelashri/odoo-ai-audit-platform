"""
SQL Query Builder

Architecture V10

Combines the SQL compiler and parameter compiler into a final executable query.
"""

from __future__ import annotations

from database.compiler.sql_compiler import SQLCompiler
from database.compiler.sql_parameter_compiler import SQLParameterCompiler


class SQLQueryBuilder:

    def __init__(self) -> None:
        self.sql_compiler = SQLCompiler()
        self.parameter_compiler = SQLParameterCompiler()

    def build(self, plan: dict) -> tuple[str, list]:

        sql = self.sql_compiler.compile(plan)
        params = self.parameter_compiler.compile(plan)

        return sql, params
