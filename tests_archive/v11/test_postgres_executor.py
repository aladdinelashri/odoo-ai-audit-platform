from unittest.mock import MagicMock, patch

from database.executor.postgres_executor import PostgreSQLExecutor


@patch("database.executor.postgres_executor.psycopg2.connect")
def test_connection(mock_connect):

    conn = MagicMock()
    mock_connect.return_value = conn

    executor = PostgreSQLExecutor(
        host="localhost",
        port=5432,
        database="test",
        user="user",
        password="pass",
    )

    assert executor.connection == conn


@patch("database.executor.postgres_executor.psycopg2.connect")
def test_execute(mock_connect):

    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchall.return_value = [
        (1,),
        (2,),
    ]

    conn.cursor.return_value.__enter__.return_value = cursor

    mock_connect.return_value = conn

    executor = PostgreSQLExecutor(
        host="localhost",
        port=5432,
        database="test",
        user="user",
        password="pass",
    )

    rows = executor.execute(
        "SELECT 1",
        [],
    )

    assert rows == [
        (1,),
        (2,),
    ]


@patch("database.executor.postgres_executor.psycopg2.connect")
def test_close(mock_connect):

    conn = MagicMock()

    mock_connect.return_value = conn

    executor = PostgreSQLExecutor(
        host="localhost",
        port=5432,
        database="test",
        user="user",
        password="pass",
    )

    executor.close()

    conn.close.assert_called_once()
