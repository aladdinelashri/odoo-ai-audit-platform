from database.query.query_analyzer import QueryAnalyzer
from database.planner.query_planner import QueryPlanner


def test_this_month_filter_planning():

    analyzer = QueryAnalyzer()
    planner = QueryPlanner()

    analysis = analyzer.analyze("show invoices this month")

    plan = planner.plan(analysis)

    assert "invoice_date >= DATE_TRUNC('month', CURRENT_DATE)" in plan["where"][0]
