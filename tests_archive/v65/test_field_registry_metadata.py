from database.metadata.field_registry import FieldRegistry


def test_field_registry_metadata():

    registry = FieldRegistry()

    fields = registry.get_fields("account.move")

    assert isinstance(fields, list)
    assert len(fields) > 10
    assert "company_id" in fields
