from database.metadata.model_registry import ModelRegistry
from database.planner.query_planner import QueryPlanner


def test_planner_uses_registry():

    registry = ModelRegistry()

    planner = QueryPlanner(model_registry=registry)

    plan = planner.plan(
        {
            "entities": ["invoice"],
            "intent": "show",
            "aggregation": None,
            "filters": [],
        }
    )

    assert plan["model"] == "account.move"
