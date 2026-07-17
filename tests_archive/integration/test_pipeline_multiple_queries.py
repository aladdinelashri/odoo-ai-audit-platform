from database.executor.postgres_executor import PostgreSQLExecutor
from database.ai.pipeline.live_pipeline import LivePipeline


def test_pipeline_multiple_queries():

    executor = PostgreSQLExecutor.from_config()

    pipeline = LivePipeline(executor)

    queries = [
        "show invoices",
        "show customers",
        "show products",
        "show journals",
    ]

    for query in queries:
        result = pipeline.ask(query)

        assert isinstance(result, dict)
        assert "sql" in result
        assert "rows" in result
        assert "columns" in result

    executor.close()
