from unittest.mock import MagicMock
import pytest

from database.executor.query_executor import QueryExecutor


def test_execute_select():
    postgres = MagicMock()
    postgres.execute.return_value = [(1,), (2,)]

    executor = QueryExecutor(postgres)

    rows = executor.execute(
        "SELECT * FROM account_move",
        [],
    )

    assert rows == [(1,), (2,)]
    postgres.execute.assert_called_once()


def test_execute_with_params():
    postgres = MagicMock()
    postgres.execute.return_value = [(100,)]

    executor = QueryExecutor(postgres)

    rows = executor.execute(
        "SELECT * FROM account_move WHERE state = %s",
        ["posted"],
    )

    assert rows == [(100,)]
    postgres.execute.assert_called_once_with(
        "SELECT * FROM account_move WHERE state = %s",
        ["posted"],
    )


def test_block_update():
    postgres = MagicMock()

    executor = QueryExecutor(postgres)

    with pytest.raises(PermissionError):
        executor.execute(
            "UPDATE account_move SET state='posted'"
        )

    postgres.execute.assert_not_called()


def test_block_delete():
    postgres = MagicMock()

    executor = QueryExecutor(postgres)

    with pytest.raises(PermissionError):
        executor.execute(
            "DELETE FROM account_move"
        )

    postgres.execute.assert_not_called()


def test_block_drop():
    postgres = MagicMock()

    executor = QueryExecutor(postgres)

    with pytest.raises(PermissionError):
        executor.execute(
            "DROP TABLE account_move"
        )

    postgres.execute.assert_not_called()
