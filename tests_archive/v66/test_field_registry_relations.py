from database.metadata.field_registry import FieldRegistry


def test_company_relation():

    registry = FieldRegistry()

    relation = registry.get_relation(
        "account.move",
        "company_id",
    )

    assert relation == "res.company"
