from database.ai.semantic.field_dictionary import FieldDictionary


def test_dictionary_returns_amount_total():

    d = FieldDictionary()

    assert d.resolve("amount") == "amount_total"


def test_dictionary_returns_invoice_date():

    d = FieldDictionary()

    assert d.resolve("date") == "invoice_date"


def test_dictionary_exists():

    d = FieldDictionary()

    assert d.exists("customer")


def test_dictionary_unknown():

    d = FieldDictionary()

    assert d.resolve("abcdef") is None


def test_dictionary_not_empty():

    d = FieldDictionary()

    assert len(d.all()) > 5
