from database.security.sql_validator import SQLValidator


def test_allow_select():

    validator = SQLValidator()

    assert validator.validate(
        "SELECT * FROM account_move"
    )


def test_block_delete():

    validator = SQLValidator()

    assert not validator.validate(
        "DELETE FROM account_move"
    )


def test_block_update():

    validator = SQLValidator()

    assert not validator.validate(
        "UPDATE account_move SET name='A'"
    )


def test_block_insert():

    validator = SQLValidator()

    assert not validator.validate(
        "INSERT INTO account_move VALUES (1)"
    )


def test_block_drop():

    validator = SQLValidator()

    assert not validator.validate(
        "DROP TABLE account_move"
    )
