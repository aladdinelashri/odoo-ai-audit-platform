from database.planner.query_planner import QueryPlanner


def test_count_aggregation_mapping():

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

    assert plan["aggregation"] == "count"
