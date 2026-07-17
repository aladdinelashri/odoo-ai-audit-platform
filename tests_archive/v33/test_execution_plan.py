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
        "table": "account.move",
        "select": ["*"],
        "from": "account_move",
        "where": ["payment_state = %s"],
        "where_values": ["not_paid"],
        "params": ["not_paid"],
        "order": [],
        "limit": None,
    }
