from database.metadata.model_registry import ModelRegistry


def test_model_registry():

    registry = ModelRegistry()

    assert registry.get_model("invoice") == "account.move"
    assert registry.get_model("customer") == "res.partner"
    assert registry.get_model("product") == "product.template"
