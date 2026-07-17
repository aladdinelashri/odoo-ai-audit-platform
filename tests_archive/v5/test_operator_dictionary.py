from database.ai.semantic.operator_dictionary import OperatorDictionary


def test_equal():
    d = OperatorDictionary()
    assert d.resolve("equals") == "="


def test_greater():
    d = OperatorDictionary()
    assert d.resolve("greater than") == ">"


def test_less():
    d = OperatorDictionary()
    assert d.resolve("less than") == "<"


def test_between():
    d = OperatorDictionary()
    assert d.resolve("between") == "BETWEEN"


def test_contains():
    d = OperatorDictionary()
    assert d.resolve("contains") == "ILIKE"


def test_exists():
    d = OperatorDictionary()
    assert d.exists("after")


def test_unknown():
    d = OperatorDictionary()
    assert d.resolve("abcdef") is None
