from database.metadata.model_registry import ModelRegistry
from database.compiler.sql_query_builder import SQLQueryBuilder


def test_dynamic_table_resolution():

    registry = ModelRegistry()

    builder = SQLQueryBuilder(model_registry=registry)

    plan = {
        "model": registry.get_model("customer"),
        "select": ["*"],
        "where": [],
        "params": [],
        "order": [],
        "limit": None,
    }

    sql, _ = builder.build(plan)

    assert "FROM res_partner" in sql
