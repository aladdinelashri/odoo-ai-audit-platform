from database.executor.postgres_executor import PostgreSQLExecutor


def test_live_query_returns_real_columns():

    executor = PostgreSQLExecutor.from_config()

    columns, rows = executor.execute_with_columns(
        """
        SELECT *
        FROM account_move
        LIMIT 1;
        """
    )

    assert len(columns) > 0
    assert "id" in columns
    assert "partner_id" in columns

    executor.close()
