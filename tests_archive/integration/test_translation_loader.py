import pytest

from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.knowledge_loader import KnowledgeLoader


def test_translation_loader_integration():

    executor = PostgreSQLExecutor.from_config()

    count = executor.execute(
        """
        SELECT COUNT(*)
        FROM mail_message_translation;
        """
    )[0][0]

    if count == 0:
        pytest.skip("No translations in this database.")

    loader = KnowledgeLoader(executor)

    translations = loader.load_translations()

    assert len(translations) > 0

    executor.close()
