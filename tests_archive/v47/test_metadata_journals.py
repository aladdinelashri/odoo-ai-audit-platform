from database.services.metadata_loader import MetadataLoader


def test_load_journals():

    loader = MetadataLoader()

    journals = loader.load_journals()

    assert isinstance(journals, list)

    assert len(journals) > 0

    assert "id" in journals[0]

    assert "name" in journals[0]
