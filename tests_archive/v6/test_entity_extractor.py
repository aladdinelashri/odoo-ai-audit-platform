from database.ai.intent.entity_extractor import EntityExtractor


def test_invoice():
    e = EntityExtractor()
    assert e.extract("show invoices") == ["account.move"]


def test_customer():
    e = EntityExtractor()
    assert e.extract("count customers") == ["res.partner"]


def test_product():
    e = EntityExtractor()
    assert e.extract("list products") == ["product.template"]


def test_payment():
    e = EntityExtractor()
    assert e.extract("show payments") == ["account.payment"]


def test_multiple():
    e = EntityExtractor()
    assert e.extract("show invoices and payments") == [
        "account.move",
        "account.payment",
    ]


def test_none():
    e = EntityExtractor()
    assert e.extract("hello world") == []
