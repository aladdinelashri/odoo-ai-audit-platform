from database.ai.pipeline.live_pipeline import LivePipeline
from database.executor.postgres_executor import PostgreSQLExecutor


def test_live_pipeline_show_invoices():

    executor = PostgreSQLExecutor.from_config()

    pipeline = LivePipeline(executor)

    result = pipeline.ask("show invoices")

    assert isinstance(result, dict)

    assert "rows" in result
    assert "summary" in result
    assert "sql" in result
    assert "params" in result

    executor.close()
