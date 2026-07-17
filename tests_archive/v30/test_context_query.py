from database.context.context_engine import ContextEngine


def test_query_preserved():

    engine = ContextEngine()

    query = "show invoices"

    result = engine.build(query)

    assert result["query"] == query
