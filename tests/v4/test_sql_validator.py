from database.core.pipeline.context import PipelineContext
from database.core.security.sql_validator import SQLValidator


def test_valid_sql():

    context = PipelineContext("show invoices")

    context.sql = "SELECT * FROM account_move LIMIT 5"

    SQLValidator().validate(context)


def test_delete_forbidden():

    context = PipelineContext("bad")

    context.sql = "DELETE FROM account_move"

    try:
        SQLValidator().validate(context)
        assert False
    except Exception:
        assert True


def test_update_forbidden():

    context = PipelineContext("bad")

    context.sql = "UPDATE account_move SET name='x'"

    try:
        SQLValidator().validate(context)
        assert False
    except Exception:
        assert True
