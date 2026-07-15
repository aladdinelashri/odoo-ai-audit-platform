from database.executor.postgres_executor import PostgreSQLExecutor
from database.ai.pipeline.live_pipeline import LivePipeline


def test_pipeline_returns_real_column_names():

    executor = PostgreSQLExecutor.from_config()

    pipeline = LivePipeline(executor)

    result = pipeline.ask("show invoices")

    assert "columns" in result

    # We should NOT receive temporary names like column_0
    assert "column_0" not in result["columns"]

    # Odoo account_move should at least expose the primary key
    assert "id" in result["columns"]

    executor.close()
