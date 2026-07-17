from database.execution.sql_executor import SQLExecutor


def test_executor_creation():

    executor = SQLExecutor()

    assert executor is not None
