from database.executor.postgres_executor import PostgreSQLExecutor
from database.ai.pipeline.live_pipeline import LivePipeline


def test_pipeline_execution():

    executor = PostgreSQLExecutor.from_config()

    pipeline = LivePipeline(executor)

    result = pipeline.ask("show invoices")

    assert isinstance(result["rows"], list)
    assert result["count"] == len(result["rows"])
    assert isinstance(result["summary"], dict)

    executor.close()
