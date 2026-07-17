from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.knowledge_loader import KnowledgeLoader


def test_load_models():

    executor = PostgreSQLExecutor.from_config()

    loader = KnowledgeLoader(executor)

    models = loader.load_models()

    assert models.exists("account.move")
    assert models.exists("res.partner")

    executor.close()


def test_load_fields():

    executor = PostgreSQLExecutor.from_config()

    loader = KnowledgeLoader(executor)

    fields = loader.load_fields()

    assert fields.exists("account.move", "partner_id")
    assert fields.exists("account.move", "journal_id")
    assert fields.exists("res.partner", "name")

    executor.close()
