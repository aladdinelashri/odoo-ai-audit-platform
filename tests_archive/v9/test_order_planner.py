from database.ai.planner.order_planner import OrderPlanner
from database.ai.query.business_query import BusinessQuery


def test_empty():
    planner = OrderPlanner()

    q = BusinessQuery()

    assert planner.build(q) == []


def test_order_name():
    planner = OrderPlanner()

    q = BusinessQuery(
        metadata={
            "order_by": "name",
        }
    )

    assert planner.build(q) == [
        "name ASC",
    ]


def test_order_amount_desc():
    planner = OrderPlanner()

    q = BusinessQuery(
        metadata={
            "order_by": "amount_total",
            "direction": "DESC",
        }
    )

    assert planner.build(q) == [
        "amount_total DESC",
    ]


def test_order_date():
    planner = OrderPlanner()

    q = BusinessQuery(
        metadata={
            "order_by": "create_date",
        }
    )

    assert planner.build(q) == [
        "create_date ASC",
    ]


def test_direction_default():
    planner = OrderPlanner()

    q = BusinessQuery(
        metadata={
            "order_by": "id",
        }
    )

    assert planner.build(q) == [
        "id ASC",
    ]
