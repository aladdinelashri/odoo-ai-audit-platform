from database.ai.intent.value_extractor import ValueExtractor


def test_paid():
    e = ValueExtractor()
    assert e.extract("paid invoices") == "posted"


def test_draft():
    e = ValueExtractor()
    assert e.extract("draft invoices") == "draft"


def test_cancelled():
    e = ValueExtractor()
    assert e.extract("cancelled invoices") == "cancel"


def test_today():
    e = ValueExtractor()
    assert e.extract("today invoices") == "today"


def test_this_month():
    e = ValueExtractor()
    assert e.extract("this month invoices") == "this_month"


def test_true():
    e = ValueExtractor()
    assert e.extract("true") is True


def test_false():
    e = ValueExtractor()
    assert e.extract("false") is False


def test_none():
    e = ValueExtractor()
    assert e.extract("show invoices") is None
