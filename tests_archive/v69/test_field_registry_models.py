from database.metadata.field_registry import FieldRegistry


def test_available_models():

    registry = FieldRegistry()

    models = registry.models()

    assert "account.move" in models
    assert "res.partner" in models
