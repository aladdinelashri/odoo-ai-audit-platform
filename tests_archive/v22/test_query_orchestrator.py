import pytest

from database.executor.postgres_executor import PostgreSQLExecutor
from database.schema.schema_loader import SchemaLoader
from database.registry.schema_registry import SchemaRegistry
from database.odoo.model_registry import ModelRegistry
from database.services.metadata_service import MetadataService
from database.security.sql_validator import SQLValidator
from database.security.schema_validator import SchemaValidator
from database.security.sql_guard import SQLGuard
from database.ai.pipeline.ai_pipeline import AIPipeline
from database.ai.pipeline.query_orchestrator import QueryOrchestrator


def test_query_orchestrator():

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

    pipeline = AIPipeline()

    orchestrator = QueryOrchestrator(
        pipeline,
        guard,
        executor,
    )

    result = orchestrator.ask("show invoices")

    assert isinstance(result, dict)
    assert "rows" in result
    assert "sql" in result
    assert "count" in result

    executor.close()
