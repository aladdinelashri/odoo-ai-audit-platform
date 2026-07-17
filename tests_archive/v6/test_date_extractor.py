from database.ai.intent.date_extractor import DateExtractor


def test_today():
    e = DateExtractor()
    assert e.extract("show invoices today") == "today"


def test_yesterday():
    e = DateExtractor()
    assert e.extract("show invoices yesterday") == "yesterday"


def test_this_month():
    e = DateExtractor()
    assert e.extract("show invoices this month") == "this_month"


def test_last_month():
    e = DateExtractor()
    assert e.extract("show invoices last month") == "last_month"


def test_this_year():
    e = DateExtractor()
    assert e.extract("show invoices this year") == "this_year"


def test_last_year():
    e = DateExtractor()
    assert e.extract("show invoices last year") == "last_year"


def test_none():
    e = DateExtractor()
    assert e.extract("show invoices") is None
