from database.ai.planner.limit_planner import LimitPlanner
from database.ai.query.business_query import BusinessQuery


def test_default_limit():
    planner = LimitPlanner()

    q = BusinessQuery()

    assert planner.build(q) == 100


def test_custom_limit():
    planner = LimitPlanner()

    q = BusinessQuery(
        metadata={
            "limit": 25,
        }
    )

    assert planner.build(q) == 25


def test_zero_limit():
    planner = LimitPlanner()

    q = BusinessQuery(
        metadata={
            "limit": 0,
        }
    )

    assert planner.build(q) == 0


def test_no_limit_for_count():
    planner = LimitPlanner()

    q = BusinessQuery(
        aggregate="count",
    )

    assert planner.build(q) is None


def test_no_limit_for_sum():
    planner = LimitPlanner()

    q = BusinessQuery(
        aggregate="sum",
    )

    assert planner.build(q) is None
