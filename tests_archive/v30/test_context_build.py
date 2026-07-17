from database.context.context_engine import ContextEngine


def test_context_build_keys():

    engine = ContextEngine()

    result = engine.build("show invoices")

    assert "query" in result
    assert "entities" in result
    assert "context" in result
