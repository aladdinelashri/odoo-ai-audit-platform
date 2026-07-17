from database.planner.query_planner import QueryPlanner


def test_filter_mapping():

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

    assert "unpaid" in plan["filters"]
