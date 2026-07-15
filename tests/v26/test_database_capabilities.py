from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.database_capabilities import DatabaseCapabilities


def test_detect_capabilities():

    executor = PostgreSQLExecutor.from_config()

    capabilities = DatabaseCapabilities(executor)

    info = capabilities.detect()

    assert isinstance(info, dict)

    assert "tables" in info

    assert "ir_model" in info["tables"]

    executor.close()
