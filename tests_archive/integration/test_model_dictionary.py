from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.knowledge_loader import KnowledgeLoader


def test_model_dictionary_integration():

    executor = PostgreSQLExecutor.from_config()

    models = KnowledgeLoader(executor).load_models()

    assert models.exists("account.move")
    assert models.exists("res.partner")
    assert models.exists("product.template")

    executor.close()
