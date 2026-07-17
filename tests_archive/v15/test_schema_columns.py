from database.executor.postgres_executor import PostgreSQLExecutor
from database.schema.schema_loader import SchemaLoader


def test_account_move_columns():

    executor = PostgreSQLExecutor.from_config()

    loader = SchemaLoader(executor)

    columns = loader.list_columns("account_move")

    assert "id" in columns
    assert "name" in columns

    executor.close()
