from database.knowledge.translation_registry import TranslationRegistry


def test_registry_creation():

    registry = TranslationRegistry()

    assert registry is not None


def test_empty_lookup():

    registry = TranslationRegistry()

    assert registry.lookup("invoice") is None
