from database.executor.postgres_executor import PostgreSQLExecutor


def test_schema_snapshot():

    executor = PostgreSQLExecutor.from_config()

    rows = executor.execute(
        """
        SELECT COUNT(*)
        FROM ir_model;
        """
    )

    assert rows[0][0] > 100

    rows = executor.execute(
        """
        SELECT COUNT(*)
        FROM ir_model_fields;
        """
    )

    assert rows[0][0] > 1000

    executor.close()
