from database.executor.postgres_executor import PostgreSQLExecutor
from database.schema.schema_loader import SchemaLoader


def test_account_move_foreign_keys():

    executor = PostgreSQLExecutor.from_config()

    loader = SchemaLoader(executor)

    fks = loader.foreign_keys("account_move")

    assert isinstance(fks, list)

    executor.close()
