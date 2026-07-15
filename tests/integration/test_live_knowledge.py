from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.knowledge_loader import KnowledgeLoader


def test_live_knowledge():

    executor = PostgreSQLExecutor.from_config()

    loader = KnowledgeLoader(executor)

    models = loader.load_models()
    fields = loader.load_fields()

    assert len(models.all()) > 100
    assert len(fields.all("account.move")) > 20

    executor.close()
