from database.compiler.sql_query_builder import SQLQueryBuilder
from database.planner.query_planner import QueryPlanner


def test_build_where_clause():

    planner = QueryPlanner()

    plan = planner.plan(
        {
            "query": "show unpaid invoices",
            "intent": "show",
            "aggregation": None,
            "entities": ["invoice"],
            "filters": ["unpaid"],
        }
    )

    builder = SQLQueryBuilder()

    sql, params = builder.build(plan)

    assert "WHERE payment_state = %s" in sql
    assert params == ["not_paid"]
