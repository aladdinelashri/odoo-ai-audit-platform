from database.compiler.sql_query_builder import SQLQueryBuilder
from database.planner.query_planner import QueryPlanner


def test_sql_builder_pipeline():

    planner = QueryPlanner()
    builder = SQLQueryBuilder()

    plan = planner.plan(
        {
            "query": "show unpaid invoices",
            "intent": "show",
            "aggregation": None,
            "entities": ["invoice"],
            "filters": ["unpaid"],
        }
    )

    sql, params = builder.build(plan)

    assert "SELECT" in sql
    assert "FROM account_move" in sql
    assert "WHERE payment_state = %s" in sql
    assert params == ["not_paid"]
