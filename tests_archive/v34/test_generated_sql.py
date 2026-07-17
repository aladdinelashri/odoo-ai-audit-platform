from database.compiler.sql_query_builder import SQLQueryBuilder
from database.planner.query_planner import QueryPlanner


def test_generated_sql_complete():

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

    expected = (
        "SELECT *\n"
        "FROM account_move\n"
        "WHERE payment_state = %s"
    )

    assert sql == expected
    assert params == ["not_paid"]
