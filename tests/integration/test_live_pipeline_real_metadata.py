from database.executor.postgres_executor import PostgreSQLExecutor
from database.ai.pipeline.live_pipeline import LivePipeline


def test_live_pipeline_uses_real_metadata():

    executor = PostgreSQLExecutor.from_config()

    pipeline = LivePipeline(executor)

    result = pipeline.ask("show invoices")

    assert "columns" in result
    assert len(result["columns"]) > 0

    # Ensure temporary names are not used
    assert "column_0" not in result["columns"]

    executor.close()
