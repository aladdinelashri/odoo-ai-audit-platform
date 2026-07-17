from database.executor.postgres_executor import PostgreSQLExecutor
from database.schema.schema_loader import SchemaLoader
from database.registry.schema_registry import SchemaRegistry


def test_registry_load():

    executor = PostgreSQLExecutor.from_config()

    loader = SchemaLoader(executor)

    registry = SchemaRegistry(loader)

    registry.load()

    assert registry.has_table("account_move")
    assert "id" in registry.columns("account_move")
    assert registry.primary_key("account_move") == "id"

    executor.close()
