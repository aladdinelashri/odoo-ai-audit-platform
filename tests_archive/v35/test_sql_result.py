from database.executor.sql_executor import SQLExecutor


def test_execute_returns_lists():

    executor = SQLExecutor()

    columns, rows = executor.execute(
        "SELECT * FROM account_move",
        [],
    )

    assert isinstance(columns, list)
    assert isinstance(rows, list)
