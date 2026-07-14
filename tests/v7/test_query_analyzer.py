from database.ai.analyzer.query_analyzer import QueryAnalyzer


def test_show():
    a = QueryAnalyzer()

    result = a.analyze("show invoices")

    assert result["intent"] == "SHOW"
    assert result["entities"] == ["account.move"]
    assert result["aggregate"] is None


def test_count():
    a = QueryAnalyzer()

    result = a.analyze("count invoices")

    assert result["intent"] == "COUNT"
    assert result["aggregate"] == "count"
    assert result["entities"] == ["account.move"]


def test_paid_today():
    a = QueryAnalyzer()

    result = a.analyze("show paid invoices today")

    assert result["intent"] == "SHOW"
    assert result["value"] == "posted"
    assert result["date"] == "today"


def test_sum():
    a = QueryAnalyzer()

    result = a.analyze("sum invoices")

    assert result["aggregate"] == "sum"


def test_max():
    a = QueryAnalyzer()

    result = a.analyze("maximum invoice amount")

    assert result["aggregate"] == "max"


def test_operator():
    a = QueryAnalyzer()

    result = a.analyze("amount greater than 100")

    assert result["operator"] == ">"


def test_unknown():
    a = QueryAnalyzer()

    result = a.analyze("hello world")

    assert result["intent"] == "UNKNOWN"
    assert result["entities"] == []
