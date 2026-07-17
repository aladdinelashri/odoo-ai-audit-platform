from database.business.business_registry import BusinessRegistry


def test_unknown_business_term():

    registry = BusinessRegistry()

    assert registry.resolve("abcdefg") is None
    assert registry.exists("abcdefg") is False
