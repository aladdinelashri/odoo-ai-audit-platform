from database.planner.query_planner import QueryPlanner


def test_invoice_model_resolution():

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

    assert plan["model"] == "account.move"
