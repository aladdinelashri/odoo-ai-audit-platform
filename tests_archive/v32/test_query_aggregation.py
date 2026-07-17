from database.query.query_analyzer import QueryAnalyzer


def test_detect_count_aggregation():

    analyzer = QueryAnalyzer()

    result = analyzer.analyze("count invoices")

    assert result["aggregation"] == "count"
