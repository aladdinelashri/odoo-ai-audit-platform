from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.database_capabilities import DatabaseCapabilities


def test_database_capabilities():

    executor = PostgreSQLExecutor.from_config()

    capabilities = DatabaseCapabilities(executor).detect()

    assert "tables" in capabilities
    assert len(capabilities["tables"]) > 0
    assert "ir_model" in capabilities["tables"]

    executor.close()
