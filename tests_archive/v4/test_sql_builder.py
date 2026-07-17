from database.core.pipeline.context import PipelineContext
from database.core.ai.query_parser import QueryParser
from database.core.planner.execution_planner import ExecutionPlanner
from database.core.sql.sql_builder import SQLBuilder


def build_sql(query):

    context = PipelineContext(query)

    QueryParser().parse(context)

    ExecutionPlanner().build(context)

    SQLBuilder().build(context)

    return context.sql


def test_sql_contains_select():

    sql = build_sql("show invoices")

    assert "SELECT" in sql


def test_sql_contains_from():

    sql = build_sql("show invoices")

    assert "FROM" in sql


def test_sql_contains_account_move():

    sql = build_sql("show invoices")

    assert "account_move" in sql
