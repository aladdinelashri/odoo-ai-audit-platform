from database.metadata.field_registry import FieldRegistry


def test_field_exists():

    registry = FieldRegistry()

    assert registry.exists(
        "account.move",
        "company_id",
    )

    assert not registry.exists(
        "account.move",
        "xxxxxxxx"
    )
