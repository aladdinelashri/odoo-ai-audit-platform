from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.knowledge_loader import KnowledgeLoader
from database.business.business_registry import BusinessRegistry


def test_business_registry_integration():

    executor = PostgreSQLExecutor.from_config()

    loader = KnowledgeLoader(executor)

    models = loader.load_models()

    registry = BusinessRegistry(models)

    assert registry.exists("invoice")
    assert registry.exists("customer")
    assert registry.exists("product")

    executor.close()
