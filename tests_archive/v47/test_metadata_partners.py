from database.services.metadata_loader import MetadataLoader


def test_load_partners():

    loader = MetadataLoader()

    partners = loader.load_partners()

    assert isinstance(partners, list)
    assert len(partners) > 0
    assert "id" in partners[0]
    assert "name" in partners[0]
