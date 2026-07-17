from database.executor.postgres_executor import PostgreSQLExecutor
from database.schema.schema_loader import SchemaLoader
from database.registry.schema_registry import SchemaRegistry
from database.odoo.model_registry import ModelRegistry
from database.services.metadata_service import MetadataService


def test_metadata_service():

    executor = PostgreSQLExecutor.from_config()

    loader = SchemaLoader(executor)

    schema = SchemaRegistry(loader)

    schema.load()

    models = ModelRegistry(schema)

    models.build()

    metadata = MetadataService(schema, models)

    assert metadata.has_model("account.move")

    assert metadata.table("account.move") == "account_move"

    assert "id" in metadata.columns("account.move")

    assert metadata.primary_key("account.move") == "id"

    executor.close()
