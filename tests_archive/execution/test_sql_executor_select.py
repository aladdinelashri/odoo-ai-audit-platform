from database.execution.sql_executor import SQLExecutor


def test_simple_select():

    executor = SQLExecutor()

    rows = executor.execute(
        "SELECT 1 AS value"
    )

    assert rows[0]["value"] == 1
