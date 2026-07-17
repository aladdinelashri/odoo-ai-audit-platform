from database.executor.sql_executor import SQLExecutor


def test_sql_executor_creation():

    executor = SQLExecutor()

    assert executor is not None
