from database.planner.query_planner import QueryPlanner


def test_execution_plan_complete():

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

    assert plan == {
        "model": "account.move",
        "operation": "show",
        "aggregation": None,
        "filters": ["unpaid"],
    }
