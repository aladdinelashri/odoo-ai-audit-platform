from database.ai.planner.where_planner import WherePlanner
from database.ai.query.business_query import BusinessQuery


def test_empty():
    planner = WherePlanner()

    q = BusinessQuery()

    assert planner.build(q) == []


def test_value_filter():
    planner = WherePlanner()

    q = BusinessQuery(
        field="state",
        operator="=",
        value="posted",
    )

    assert planner.build(q) == [
        "state = %s",
    ]


def test_today():
    planner = WherePlanner()

    q = BusinessQuery(
        date="today",
    )

    assert planner.build(q) == [
        "DATE(create_date)=CURRENT_DATE",
    ]


def test_this_month():
    planner = WherePlanner()

    q = BusinessQuery(
        date="this_month",
    )

    assert len(planner.build(q)) == 1


def test_two_conditions():
    planner = WherePlanner()

    q = BusinessQuery(
        field="state",
        operator="=",
        value="posted",
        date="today",
    )

    assert len(planner.build(q)) == 2
