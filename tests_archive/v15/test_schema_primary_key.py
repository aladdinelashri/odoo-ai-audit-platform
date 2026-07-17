from database.executor.postgres_executor import PostgreSQLExecutor
from database.schema.schema_loader import SchemaLoader


def test_account_move_primary_key():

    executor = PostgreSQLExecutor.from_config()

    loader = SchemaLoader(executor)

    pk = loader.primary_key("account_move")

    assert pk == "id"

    executor.close()
