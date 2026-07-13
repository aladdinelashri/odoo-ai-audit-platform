from database.core.ai.query_parser import QueryParser


def test_parser_returns_dict():

    parser = QueryParser()

    result = parser.parse("show invoices")

    assert isinstance(result, dict)


def test_parser_contains_intent():

    parser = QueryParser()

    result = parser.parse("show invoices")

    assert "intent" in result


def test_parser_contains_entities():

    parser = QueryParser()

    result = parser.parse("show invoices")

    assert "entities" in result


def test_parser_contains_filters():

    parser = QueryParser()

    result = parser.parse("show invoices")

    assert "filters" in result
