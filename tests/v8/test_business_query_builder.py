from database.ai.query.business_query_builder import BusinessQueryBuilder


def test_show():
    builder = BusinessQueryBuilder()

    q = builder.build("show invoices")

    assert q.intent == "SHOW"
    assert q.entities == ["account.move"]
    assert q.aggregate is None


def test_count():
    builder = BusinessQueryBuilder()

    q = builder.build("count invoices")

    assert q.intent == "COUNT"
    assert q.aggregate == "count"


def test_paid_today():
    builder = BusinessQueryBuilder()

    q = builder.build("show paid invoices today")

    assert q.value == "posted"
    assert q.date == "today"


def test_operator():
    builder = BusinessQueryBuilder()

    q = builder.build("amount greater than 100")

    assert q.operator == ">"


def test_unknown():
    builder = BusinessQueryBuilder()

    q = builder.build("hello world")

    assert q.intent == "UNKNOWN"
