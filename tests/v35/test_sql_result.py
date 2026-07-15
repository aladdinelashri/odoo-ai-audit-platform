from database.executor.sql_executor import SQLExecutor


def test_execute_returns_list():

    executor = SQLExecutor()

    result = executor.execute(
        "SELECT * FROM account_move",
        [],
    )

    assert isinstance(result, list)
