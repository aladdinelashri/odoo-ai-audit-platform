from database.business.business_registry import BusinessRegistry


def test_registry_contains_core_business_terms():

    registry = BusinessRegistry()

    expected = [
        "invoice",
        "customer",
        "partner",
        "product",
        "category",
        "journal",
        "order",
        "orders",
        "pos",
    ]

    for term in expected:
        assert registry.exists(term)
