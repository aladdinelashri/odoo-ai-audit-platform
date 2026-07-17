from database.planner.query_planner import QueryPlanner


def test_query_planner_creation():

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

    assert isinstance(plan, dict)
    assert "model" in plan
    assert "operation" in plan
    assert "filters" in plan
