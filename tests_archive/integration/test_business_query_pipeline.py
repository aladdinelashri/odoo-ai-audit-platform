from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.knowledge_loader import KnowledgeLoader
from database.business.business_registry import BusinessRegistry
from database.ai.pipeline.ai_pipeline import AIPipeline


def test_business_query_pipeline():

    executor = PostgreSQLExecutor.from_config()

    loader = KnowledgeLoader(executor)

    models = loader.load_models()

    registry = BusinessRegistry(models)

    pipeline = AIPipeline()

    plan = pipeline.analyze("show invoices")

    assert plan["sql"] is not None
    assert "account_move" in plan["sql"]

    assert registry.resolve("invoice") == "account.move"

    executor.close()
