from database.ai.semantic.model_dictionary import ModelDictionary


def test_invoice():

    d = ModelDictionary()

    assert d.resolve("invoice") == "account.move"


def test_invoices():

    d = ModelDictionary()

    assert d.resolve("invoices") == "account.move"


def test_customer():

    d = ModelDictionary()

    assert d.resolve("customer") == "res.partner"


def test_product():

    d = ModelDictionary()

    assert d.resolve("product") == "product.template"


def test_unknown():

    d = ModelDictionary()

    assert d.resolve("xxxxxxxx") is None
