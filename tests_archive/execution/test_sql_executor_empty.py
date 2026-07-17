from database.execution.sql_executor import SQLExecutor


def test_empty_result():

    executor = SQLExecutor()

    rows = executor.execute(
        "SELECT 1 WHERE FALSE"
    )

    assert rows == []
