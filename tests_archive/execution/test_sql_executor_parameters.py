from database.execution.sql_executor import SQLExecutor


def test_parameterized_query():

    executor = SQLExecutor()

    rows = executor.execute(
        "SELECT %s AS value",
        [100],
    )

    assert rows[0]["value"] == 100
