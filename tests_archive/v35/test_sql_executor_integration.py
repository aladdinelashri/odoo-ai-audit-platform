from database.planner.query_planner import QueryPlanner
from database.compiler.sql_query_builder import SQLQueryBuilder
from database.executor.sql_executor import SQLExecutor


def test_sql_pipeline():

    planner = QueryPlanner()
    builder = SQLQueryBuilder()
    executor = SQLExecutor()

    plan = planner.plan(
        {
            "query": "show invoices",
            "intent": "show",
            "aggregation": None,
            "entities": ["invoice"],
            "filters": [],
        }
    )

    sql, params = builder.build(plan)

    columns, rows = executor.execute(sql, params)

    assert isinstance(columns, list)
    assert isinstance(rows, list)
