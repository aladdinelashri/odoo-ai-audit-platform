from database.executor.postgres_executor import PostgreSQLExecutor


def test_live_sql_execution():

    executor = PostgreSQLExecutor.from_config()

    rows = executor.execute(
        """
        SELECT id
        FROM account_move
        LIMIT 5;
        """
    )

    assert isinstance(rows, list)
    assert len(rows) <= 5

    executor.close()
