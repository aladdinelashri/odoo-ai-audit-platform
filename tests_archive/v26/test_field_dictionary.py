from database.knowledge.field_dictionary import FieldDictionary


def test_add_field():

    fields = FieldDictionary()

    fields.add(
        model="account.move",
        field="partner_id",
        label="Customer",
    )

    assert fields.exists("account.move", "partner_id")

    data = fields.get("account.move", "partner_id")

    assert data["label"] == "Customer"


def test_all_fields():

    fields = FieldDictionary()

    fields.add("account.move", "partner_id", "Customer")
    fields.add("account.move", "journal_id", "Journal")

    assert len(fields.all("account.move")) == 2
