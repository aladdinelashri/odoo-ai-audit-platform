from database.services.metadata_loader import MetadataLoader


def test_load_companies():

    loader = MetadataLoader()

    companies = loader.load_companies()

    assert isinstance(companies, list)

    assert len(companies) > 0

    assert isinstance(companies[0], dict)

    assert "id" in companies[0]

    assert "name" in companies[0]
