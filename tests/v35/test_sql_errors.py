from database.executor.sql_executor import SQLExecutor


def test_execute_invalid_sql():

    executor = SQLExecutor()

    result = executor.execute(
        "",
        [],
    )

    assert result == []
