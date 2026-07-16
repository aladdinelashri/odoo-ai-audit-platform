from database.connection.postgres_connection import PostgreSQLConnection


def test_connection_has_open():

    connection = PostgreSQLConnection()

    assert hasattr(connection, "open")
