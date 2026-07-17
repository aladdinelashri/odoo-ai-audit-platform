from database.ai.semantic.value_dictionary import ValueDictionary


def test_paid():
    d = ValueDictionary()
    assert d.resolve("paid") == "posted"


def test_draft():
    d = ValueDictionary()
    assert d.resolve("draft") == "draft"


def test_cancelled():
    d = ValueDictionary()
    assert d.resolve("cancelled") == "cancel"


def test_today():
    d = ValueDictionary()
    assert d.exists("today")


def test_this_month():
    d = ValueDictionary()
    assert d.exists("this month")


def test_true():
    d = ValueDictionary()
    assert d.resolve("true") is True


def test_false():
    d = ValueDictionary()
    assert d.resolve("false") is False


def test_unknown():
    d = ValueDictionary()
    assert d.resolve("abcdef") is None
