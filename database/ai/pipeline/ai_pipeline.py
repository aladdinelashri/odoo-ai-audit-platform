"""
AI Pipeline

Architecture V13

Main orchestration layer for the AI Audit Platform.
"""

from __future__ import annotations

from database.ai.analyzer.query_analyzer import QueryAnalyzer
from database.ai.query.business_query_builder import BusinessQueryBuilder
from database.ai.planner.sql_intent_planner import SQLIntentPlanner
from database.compiler.sql_query_builder import SQLQueryBuilder


class AIPipeline:

    def __init__(self) -> None:

        self.analyzer = QueryAnalyzer()
        self.business_builder = BusinessQueryBuilder()
        self.sql_planner = SQLIntentPlanner()
        self.sql_builder = SQLQueryBuilder()

    # ---------------------------------------------------------

    def analyze(self, question: str):

        analysis = self.analyzer.analyze(question)

        business_query = self.business_builder.build(analysis)

        sql_plan = self.sql_planner.build(business_query)

        sql, params = self.sql_builder.build(sql_plan)

        return {
            "analysis": analysis,
            "business_query": business_query,
            "sql_plan": sql_plan,
            "sql": sql,
            "params": params,
        }
