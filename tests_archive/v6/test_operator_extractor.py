from database.ai.intent.operator_extractor import OperatorExtractor


def test_greater():
    e = OperatorExtractor()
    assert e.extract("amount greater than 100") == ">"


def test_less():
    e = OperatorExtractor()
    assert e.extract("amount less than 100") == "<"


def test_equals():
    e = OperatorExtractor()
    assert e.extract("amount equals 100") == "="


def test_not_equal():
    e = OperatorExtractor()
    assert e.extract("amount not equal 100") == "!="


def test_between():
    e = OperatorExtractor()
    assert e.extract("between 1 and 10") == "BETWEEN"


def test_contains():
    e = OperatorExtractor()
    assert e.extract("description contains abc") == "ILIKE"


def test_none():
    e = OperatorExtractor()
    assert e.extract("show invoices") is None
