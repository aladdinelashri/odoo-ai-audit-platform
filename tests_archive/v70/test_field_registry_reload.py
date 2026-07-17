from database.metadata.field_registry import FieldRegistry


def test_reload():

    registry = FieldRegistry()

    registry.reload()

    assert len(registry.models()) > 0
