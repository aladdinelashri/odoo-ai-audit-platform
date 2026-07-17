from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.knowledge_loader import KnowledgeLoader


def test_field_dictionary_integration():

    executor = PostgreSQLExecutor.from_config()

    fields = KnowledgeLoader(executor).load_fields()

    assert fields.exists("account.move", "partner_id")
    assert fields.exists("account.move", "move_type")
    assert fields.exists("account.move", "invoice_date")

    executor.close()
