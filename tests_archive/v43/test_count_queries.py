from database.query.query_analyzer import QueryAnalyzer
from database.planner.query_planner import QueryPlanner
from database.compiler.sql_query_builder import SQLQueryBuilder


def test_count_invoices_sql():

    analyzer = QueryAnalyzer()
    planner = QueryPlanner()
    builder = SQLQueryBuilder()

    analysis = analyzer.analyze("count invoices")
    plan = planner.plan(analysis)

    sql, params = builder.build(plan)

    assert "COUNT" in sql.upper()
