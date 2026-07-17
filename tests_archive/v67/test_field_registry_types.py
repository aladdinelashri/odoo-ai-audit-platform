from database.metadata.field_registry import FieldRegistry


def test_company_field_type():

    registry = FieldRegistry()

    field_type = registry.get_type(
        "account.move",
        "company_id",
    )

    assert field_type == "many2one"
