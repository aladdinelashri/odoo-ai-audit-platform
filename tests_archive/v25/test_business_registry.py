from database.business.business_registry import BusinessRegistry


def test_invoice_mapping():

    registry = BusinessRegistry()

    assert registry.resolve("invoice") == "account.move"

    assert registry.resolve("invoices") == "account.move"

    assert registry.resolve("bill") == "account.move"

    assert registry.resolve("journal") == "account.journal"

    assert registry.resolve("customer") == "res.partner"

    assert registry.resolve("product") == "product.template"
