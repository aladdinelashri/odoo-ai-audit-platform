from database.query.query_analyzer import QueryAnalyzer


def test_query_analyzer_creation():

    analyzer = QueryAnalyzer()

    result = analyzer.analyze("show invoices")

    assert isinstance(result, dict)
    assert "query" in result
    assert "intent" in result
    assert "entities" in result
    assert "filters" in result
