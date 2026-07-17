from database.metadata.model_registry import ModelRegistry
from database.compiler.sql_query_builder import SQLQueryBuilder


def test_sql_builder_registry():

    registry = ModelRegistry()

    builder = SQLQueryBuilder(model_registry=registry)

    plan = {
        "model": registry.get_model("invoice"),
        "from": "account_move",
        "select": ["*"],
        "where": [],
        "params": [],
        "order": [],
        "limit": None,
    }

    sql, params = builder.build(plan)

    assert "FROM account_move" in sql
