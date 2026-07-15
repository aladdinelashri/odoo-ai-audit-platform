from database.executor.postgres_executor import PostgreSQLExecutor
from database.schema.schema_loader import SchemaLoader


def test_list_tables():

    executor = PostgreSQLExecutor.from_config()

    loader = SchemaLoader(executor)

    tables = loader.list_tables()

    assert "account_move" in tables
    assert "account_move_line" in tables
    assert len(tables) > 100

    executor.close()
