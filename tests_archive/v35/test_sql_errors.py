from database.executor.sql_executor import SQLExecutor


def test_execute_invalid_sql():

    executor = SQLExecutor()

    columns, rows = executor.execute(
        "",
        [],
    )

    assert columns == []
    assert rows == []
