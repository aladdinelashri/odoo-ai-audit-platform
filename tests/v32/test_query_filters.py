from database.query.query_analyzer import QueryAnalyzer


def test_detect_unpaid_filter():

    analyzer = QueryAnalyzer()

    result = analyzer.analyze("show unpaid invoices")

    assert "unpaid" in result["filters"]
