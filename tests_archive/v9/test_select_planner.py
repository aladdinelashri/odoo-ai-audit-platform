from database.ai.planner.select_planner import SelectPlanner
from database.ai.query.business_query import BusinessQuery


def test_default_select():
    planner = SelectPlanner()

    q = BusinessQuery()

    assert planner.build(q) == ["*"]


def test_count():
    planner = SelectPlanner()

    q = BusinessQuery(
        aggregate="count",
    )

    assert planner.build(q) == ["COUNT(*)"]


def test_sum():
    planner = SelectPlanner()

    q = BusinessQuery(
        aggregate="sum",
        field="amount_total",
    )

    assert planner.build(q) == ["SUM(amount_total)"]


def test_avg():
    planner = SelectPlanner()

    q = BusinessQuery(
        aggregate="avg",
        field="amount_total",
    )

    assert planner.build(q) == ["AVG(amount_total)"]


def test_min():
    planner = SelectPlanner()

    q = BusinessQuery(
        aggregate="min",
        field="amount_total",
    )

    assert planner.build(q) == ["MIN(amount_total)"]


def test_max():
    planner = SelectPlanner()

    q = BusinessQuery(
        aggregate="max",
        field="amount_total",
    )

    assert planner.build(q) == ["MAX(amount_total)"]
