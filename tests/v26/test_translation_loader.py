from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.knowledge_loader import KnowledgeLoader


def test_load_translations():

    executor = PostgreSQLExecutor.from_config()

    loader = KnowledgeLoader(executor)

    translations = loader.load_translations()

    assert isinstance(translations, list)

    executor.close()
