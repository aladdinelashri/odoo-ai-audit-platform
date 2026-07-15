from database.executor.sql_executor import SQLExecutor


def test_execute_returns_result():

    executor = SQLExecutor()

    result = executor.execute(
        "SELECT 1",
        []
    )

    assert result == []
