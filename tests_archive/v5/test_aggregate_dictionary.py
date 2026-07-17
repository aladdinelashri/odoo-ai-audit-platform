from database.ai.semantic.aggregate_dictionary import AggregateDictionary


def test_count():
    d = AggregateDictionary()
    assert d.resolve("count") == "count"


def test_sum():
    d = AggregateDictionary()
    assert d.resolve("sum") == "sum"


def test_average():
    d = AggregateDictionary()
    assert d.resolve("average") == "avg"


def test_exists():
    d = AggregateDictionary()
    assert d.exists("maximum")


def test_unknown():
    d = AggregateDictionary()
    assert d.resolve("abcdef") is None
