from database.executor.postgres_executor import PostgreSQLExecutor
from database.schema.schema_loader import SchemaLoader
from database.registry.schema_registry import SchemaRegistry
from database.odoo.model_registry import ModelRegistry


def test_model_registry():

    executor = PostgreSQLExecutor.from_config()

    loader = SchemaLoader(executor)

    registry = SchemaRegistry(loader)

    registry.load()

    models = ModelRegistry(registry)

    models.build()

    assert models.has_model("account.move")

    assert models.table("account.move") == "account_move"

    executor.close()
