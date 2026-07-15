from database.executor.postgres_executor import PostgreSQLExecutor
from database.ai.pipeline.live_pipeline import LivePipeline


def test_pipeline_sql_validity():

    executor = PostgreSQLExecutor.from_config()

    pipeline = LivePipeline(executor)

    result = pipeline.ask("show invoices")

    sql = result["sql"].lower()

    assert "select" in sql
    assert "from" in sql
    assert "account_move" in sql

    executor.close()
