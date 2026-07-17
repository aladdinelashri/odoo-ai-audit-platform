from database.executor.postgres_executor import PostgreSQLExecutor
from database.schema.schema_loader import SchemaLoader
from database.registry.schema_registry import SchemaRegistry
from database.odoo.model_registry import ModelRegistry
from database.services.metadata_service import MetadataService
from database.security.schema_validator import SchemaValidator


def test_schema_validator():

    executor = PostgreSQLExecutor.from_config()

    loader = SchemaLoader(executor)

    schema = SchemaRegistry(loader)

    schema.load()

    models = ModelRegistry(schema)

    models.build()

    metadata = MetadataService(schema, models)

    validator = SchemaValidator(metadata)

    assert validator.table_exists("account.move")

    assert validator.column_exists("account.move", "id")

    assert not validator.column_exists("account.move", "this_column_does_not_exist")

    executor.close()
