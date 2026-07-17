import pytest

from database.executor.safe_executor import SafeExecutor


def test_select_allowed():
    executor = SafeExecutor()

    assert executor.validate("SELECT * FROM account_move")


def test_with_allowed():
    executor = SafeExecutor()

    assert executor.validate(
        "WITH t AS (SELECT 1) SELECT * FROM t"
    )


def test_explain_allowed():
    executor = SafeExecutor()

    assert executor.validate(
        "EXPLAIN SELECT * FROM account_move"
    )


@pytest.mark.parametrize(
    "sql",
    [
        "INSERT INTO account_move VALUES (1)",
        "UPDATE account_move SET state='posted'",
        "DELETE FROM account_move",
        "DROP TABLE account_move",
        "ALTER TABLE account_move ADD COLUMN x INT",
        "TRUNCATE TABLE account_move",
        "CREATE TABLE demo(id INT)",
        "GRANT ALL ON account_move TO user1",
        "REVOKE ALL ON account_move FROM user1",
    ],
)
def test_blocked_statements(sql):
    executor = SafeExecutor()

    with pytest.raises(PermissionError):
        executor.validate(sql)


def test_unknown_statement():
    executor = SafeExecutor()

    with pytest.raises(PermissionError):
        executor.validate("VACUUM account_move")
