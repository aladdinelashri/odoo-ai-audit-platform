from database.ai.planner.from_planner import FromPlanner
from database.ai.query.business_query import BusinessQuery


def test_invoice():
    planner = FromPlanner()

    q = BusinessQuery(
        entities=["account.move"],
    )

    assert planner.build(q) == "account.move"


def test_partner():
    planner = FromPlanner()

    q = BusinessQuery(
        entities=["res.partner"],
    )

    assert planner.build(q) == "res.partner"


def test_product():
    planner = FromPlanner()

    q = BusinessQuery(
        entities=["product.template"],
    )

    assert planner.build(q) == "product.template"


def test_pos():
    planner = FromPlanner()

    q = BusinessQuery(
        entities=["pos.order"],
    )

    assert planner.build(q) == "pos.order"


def test_no_entity():

    planner = FromPlanner()

    q = BusinessQuery()

    try:
        planner.build(q)
        assert False
    except ValueError:
        assert True
