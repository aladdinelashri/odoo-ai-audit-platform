from database.query.query_analyzer import QueryAnalyzer


def test_detect_invoice_entity():

    analyzer = QueryAnalyzer()

    result = analyzer.analyze("show invoices")

    assert "invoice" in result["entities"]
