from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.knowledge_loader import KnowledgeLoader


def test_metadata_consistency():

    executor = PostgreSQLExecutor.from_config()

    loader = KnowledgeLoader(executor)

    models = loader.load_models()
    fields = loader.load_fields()

    for model in [
        "account.move",
        "res.partner",
        "product.template",
        "pos.order",
    ]:
        assert models.exists(model)
        assert len(fields.all(model)) > 0

    executor.close()
