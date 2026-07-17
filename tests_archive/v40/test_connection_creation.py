from database.connection.postgres_connection import PostgreSQLConnection


def test_connection_creation():

    connection = PostgreSQLConnection()

    assert connection is not None
