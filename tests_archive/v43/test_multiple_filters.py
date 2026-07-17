from database.query.query_analyzer import QueryAnalyzer
from database.planner.query_planner import QueryPlanner
from database.compiler.sql_query_builder import SQLQueryBuilder


def test_count_unpaid_invoices():

    analyzer = QueryAnalyzer()
    planner = QueryPlanner()
    builder = SQLQueryBuilder()

    analysis = analyzer.analyze("count unpaid invoices")
    plan = planner.plan(analysis)

    sql, params = builder.build(plan)

    assert "COUNT" in sql.upper()
    assert "PAYMENT_STATE" in sql.upper()
    assert params == ["not_paid"]
