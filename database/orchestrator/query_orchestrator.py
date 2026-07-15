"""
Query Orchestrator

Architecture V39
"""

from __future__ import annotations

from database.query.query_analyzer import QueryAnalyzer
from database.planner.query_planner import QueryPlanner
from database.compiler.sql_query_builder import SQLQueryBuilder
from database.executor.sql_executor import SQLExecutor
from database.formatter.result_formatter import ResultFormatter


class QueryOrchestrator:

    def __init__(self) -> None:

        self.analyzer = QueryAnalyzer()
        self.planner = QueryPlanner()
        self.builder = SQLQueryBuilder()
        self.executor = SQLExecutor()
        self.formatter = ResultFormatter()

    def run(self, query: str) -> dict:

        analysis = self.analyzer.analyze(query)

        plan = self.planner.plan(analysis)

        sql, params = self.builder.build(plan)

        columns, rows = self.executor.execute(sql, params)

        return self.formatter.format(columns, rows)
