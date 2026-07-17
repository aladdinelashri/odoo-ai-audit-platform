from database.executor.postgres_executor import PostgreSQLExecutor
from database.ai.pipeline.live_pipeline import LivePipeline


def test_live_query_pipeline():

    executor = PostgreSQLExecutor.from_config()

    pipeline = LivePipeline(executor)

    result = pipeline.ask("show invoices")

    assert isinstance(result, dict)
    assert "sql" in result
    assert "columns" in result
    assert "rows" in result
    assert "summary" in result

    executor.close()
