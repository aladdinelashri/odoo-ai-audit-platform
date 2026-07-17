from database.connection.postgres_connection import PostgreSQLConnection


def test_connection_has_config():

    connection = PostgreSQLConnection()

    assert hasattr(connection, "config")
    assert isinstance(connection.config, dict)
