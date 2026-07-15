from database.compiler.sql_query_builder import SQLQueryBuilder
from database.planner.query_planner import QueryPlanner


def test_build_simple_select():

    planner = QueryPlanner()

    plan = planner.plan(
        {
            "query": "show invoices",
            "intent": "show",
            "aggregation": None,
            "entities": ["invoice"],
            "filters": [],
        }
    )

    builder = SQLQueryBuilder()

    sql, params = builder.build(plan)

    assert sql == "SELECT *\nFROM account_move"
    assert params == []
