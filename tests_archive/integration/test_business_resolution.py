from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.knowledge_loader import KnowledgeLoader
from database.business.business_registry import BusinessRegistry


def test_business_resolution():

    executor = PostgreSQLExecutor.from_config()

    models = KnowledgeLoader(executor).load_models()

    registry = BusinessRegistry(models)

    assert registry.resolve("invoice") == "account.move"
    assert registry.resolve("customer") == "res.partner"
    assert registry.resolve("product") == "product.template"
    assert registry.resolve("orders") == "pos.order"

    executor.close()
