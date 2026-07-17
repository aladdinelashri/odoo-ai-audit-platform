from database.ai.planner.sql_plan_builder import SQLPlanBuilder
from database.ai.query.business_query import BusinessQuery


def test_simple_query():
    planner = SQLPlanBuilder()

    q = BusinessQuery(
        entities=["account.move"],
    )

    plan = planner.build(q)

    assert plan["select"] == ["*"]
    assert plan["from"] == "account.move"
    assert plan["where"] == []
    assert plan["order"] == []
    assert plan["limit"] == 100


def test_count_query():
    planner = SQLPlanBuilder()

    q = BusinessQuery(
        entities=["account.move"],
        aggregate="count",
    )

    plan = planner.build(q)

    assert plan["select"] == ["COUNT(*)"]
    assert plan["limit"] is None


def test_sum_query():
    planner = SQLPlanBuilder()

    q = BusinessQuery(
        entities=["account.move"],
        aggregate="sum",
        field="amount_total",
    )

    plan = planner.build(q)

    assert plan["select"] == ["SUM(amount_total)"]


def test_filtered_query():
    planner = SQLPlanBuilder()

    q = BusinessQuery(
        entities=["account.move"],
        field="state",
        operator="=",
        value="posted",
    )

    plan = planner.build(q)

    assert plan["where"] == ["state = %s"]


def test_order_query():
    planner = SQLPlanBuilder()

    q = BusinessQuery(
        entities=["account.move"],
        metadata={
            "order_by": "create_date",
            "direction": "DESC",
        },
    )

    plan = planner.build(q)

    assert plan["order"] == ["create_date DESC"]


def test_limit_query():
    planner = SQLPlanBuilder()

    q = BusinessQuery(
        entities=["account.move"],
        metadata={
            "limit": 10,
        },
    )

    plan = planner.build(q)

    assert plan["limit"] == 10
