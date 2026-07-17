from database.metadata.field_registry import FieldRegistry


def test_invoice_fields():

    registry = FieldRegistry()

    fields = registry.get_fields("account.move")

    assert "company_id" in fields
    assert "partner_id" in fields
