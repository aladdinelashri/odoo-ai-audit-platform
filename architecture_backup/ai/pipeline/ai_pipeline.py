"""
AI Pipeline

Architecture V22
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

    def analyze(self, question: str) -> dict:

        analysis = self.analyzer.analyze(question)

        business_query = self.business_builder.build(analysis)

        sql_plan = self.sql_planner.build(business_query)

        sql, params = self.sql_builder.build(sql_plan)

        return {
            "intent": analysis.get("intent"),
            "confidence": analysis.get("confidence"),
            "entities": analysis.get("entities"),
            "analysis": analysis,
            "business_query": business_query,
            "sql_plan": sql_plan,
            "model": business_query.entities[0] if business_query.entities else None,
            "sql": sql,
            "params": params,
        }
