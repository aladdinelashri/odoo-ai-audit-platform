from database.executor.postgres_executor import PostgreSQLExecutor
from database.schema.schema_loader import SchemaLoader
from database.registry.schema_registry import SchemaRegistry
from database.odoo.model_registry import ModelRegistry
from database.services.metadata_service import MetadataService
from database.security.sql_validator import SQLValidator
from database.security.schema_validator import SchemaValidator
from database.security.sql_guard import SQLGuard


def test_sql_guard():

    executor = PostgreSQLExecutor.from_config()

    loader = SchemaLoader(executor)

    schema = SchemaRegistry(loader)

    schema.load()

    models = ModelRegistry(schema)

    models.build()

    metadata = MetadataService(schema, models)

    guard = SQLGuard(
        SQLValidator(),
        SchemaValidator(metadata),
    )

    assert guard.validate(
        "account.move",
        "SELECT id,name FROM account_move",
    )

    assert not guard.validate(
        "account.move",
        "SELECT fake_column FROM account_move",
    )

    assert not guard.validate(
        "account.move",
        "DELETE FROM account_move",
    )

    executor.close()
