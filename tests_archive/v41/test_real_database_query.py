from database.executor.sql_executor import SQLExecutor


def test_real_database_query():

    executor = SQLExecutor()

    columns, rows = executor.execute(
        "SELECT id, name FROM account_move LIMIT 5",
        [],
    )

    assert isinstance(columns, list)
    assert isinstance(rows, list)
