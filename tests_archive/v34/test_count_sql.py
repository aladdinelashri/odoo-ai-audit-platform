from database.compiler.sql_query_builder import SQLQueryBuilder
from database.planner.query_planner import QueryPlanner


def test_build_count_sql():

    planner = QueryPlanner()

    plan = planner.plan(
        {
            "query": "count invoices",
            "intent": None,
            "aggregation": "count",
            "entities": ["invoice"],
            "filters": [],
        }
    )

    if plan["aggregation"] == "count":
        plan["select"] = ["COUNT(*)"]

    builder = SQLQueryBuilder()

    sql, params = builder.build(plan)

    assert sql == "SELECT COUNT(*)\nFROM account_move"
    assert params == []
