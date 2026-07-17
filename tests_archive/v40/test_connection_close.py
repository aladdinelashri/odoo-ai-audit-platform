from database.connection.postgres_connection import PostgreSQLConnection


def test_connection_has_close():

    connection = PostgreSQLConnection()

    assert hasattr(connection, "close")
