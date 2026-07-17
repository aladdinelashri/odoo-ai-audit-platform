from database.ai.intent.aggregate_extractor import AggregateExtractor


def test_count():
    e = AggregateExtractor()
    assert e.extract("count invoices") == "count"


def test_sum():
    e = AggregateExtractor()
    assert e.extract("sum invoices") == "sum"


def test_average():
    e = AggregateExtractor()
    assert e.extract("average invoice amount") == "avg"


def test_min():
    e = AggregateExtractor()
    assert e.extract("minimum invoice amount") == "min"


def test_max():
    e = AggregateExtractor()
    assert e.extract("maximum invoice amount") == "max"


def test_none():
    e = AggregateExtractor()
    assert e.extract("show invoices") is None
