from database.executor.postgres_executor import PostgreSQLExecutor
from database.ai.pipeline.live_pipeline import LivePipeline


def test_live_pipeline_returns_structured_result():

    executor = PostgreSQLExecutor.from_config()

    pipeline = LivePipeline(executor)

    result = pipeline.ask("show invoices")

    assert isinstance(result, dict)

    assert "columns" in result

    assert "rows" in result

    assert "count" in result

    executor.close()
