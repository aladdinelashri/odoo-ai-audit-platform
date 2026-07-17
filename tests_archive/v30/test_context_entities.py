from database.context.context_engine import ContextEngine


def test_entities_is_list():

    engine = ContextEngine()

    result = engine.build("show invoices")

    assert isinstance(result["entities"], list)
