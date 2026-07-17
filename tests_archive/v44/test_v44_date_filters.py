from database.query.query_analyzer import QueryAnalyzer
from database.planner.query_planner import QueryPlanner
from database.compiler.sql_query_builder import SQLQueryBuilder


def test_show_invoices_this_month():

    analyzer = QueryAnalyzer()
    planner = QueryPlanner()
    builder = SQLQueryBuilder()

    analysis = analyzer.analyze("show invoices this month")

    plan = planner.plan(analysis)

    sql, params = builder.build(plan)

    assert "invoice" in analysis["entities"]
    assert "this_month" in analysis["filters"]
