from database.core.pipeline.context import PipelineContext
from database.core.sql.sql_executor import SQLExecutor


def test_sql_executor_returns_rows():

    context = PipelineContext("show invoices")

    context.sql = "SELECT id FROM account_move LIMIT 5"

    rows = SQLExecutor().execute(context)

    assert isinstance(rows, list)


def test_sql_executor_not_empty():

    context = PipelineContext("show invoices")

    context.sql = "SELECT id FROM account_move LIMIT 5"

    rows = SQLExecutor().execute(context)

    assert len(rows) > 0


def test_sql_executor_row_type():

    context = PipelineContext("show invoices")

    context.sql = "SELECT id FROM account_move LIMIT 1"

    rows = SQLExecutor().execute(context)

    assert isinstance(rows[0], dict)
