from database.ai.semantic.semantic_resolver import SemanticResolver


def test_model():
    r = SemanticResolver()
    assert r.resolve_model("invoice") == "account.move"


def test_field():
    r = SemanticResolver()
    assert r.resolve_field("amount")


def test_operator():
    r = SemanticResolver()
    assert r.resolve_operator("greater than") == ">"


def test_aggregate():
    r = SemanticResolver()
    assert r.resolve_aggregate("count") == "count"


def test_value():
    r = SemanticResolver()
    assert r.resolve_value("paid") == "posted"
