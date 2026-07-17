from database.ai.query.business_query_builder import BusinessQueryBuilder
from database.ai.planner.sql_intent_planner import SQLIntentPlanner


def test_show():
    builder = BusinessQueryBuilder()
    planner = SQLIntentPlanner()

    q = builder.build("show invoices")
    plan = planner.build(q)

    assert plan["intent"] == "SHOW"
    assert plan["table"] == "account.move"


def test_count():
    builder = BusinessQueryBuilder()
    planner = SQLIntentPlanner()

    q = builder.build("count invoices")
    plan = planner.build(q)

    assert plan["aggregate"] == "count"


def test_paid():
    builder = BusinessQueryBuilder()
    planner = SQLIntentPlanner()

    q = builder.build("show paid invoices")
    plan = planner.build(q)

    assert plan["value"] == "posted"


def test_today():
    builder = BusinessQueryBuilder()
    planner = SQLIntentPlanner()

    q = builder.build("show invoices today")
    plan = planner.build(q)

    assert plan["date"] == "today"


def test_no_entity():
    builder = BusinessQueryBuilder()
    planner = SQLIntentPlanner()

    try:
        planner.build(builder.build("hello world"))
        assert False
    except ValueError:
        assert True
