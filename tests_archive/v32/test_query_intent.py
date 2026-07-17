from database.query.query_analyzer import QueryAnalyzer


def test_detect_show_intent():

    analyzer = QueryAnalyzer()

    result = analyzer.analyze("show invoices")

    assert result["intent"] == "show"
