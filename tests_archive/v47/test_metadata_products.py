from database.services.metadata_loader import MetadataLoader


def test_load_products():

    loader = MetadataLoader()

    products = loader.load_products()

    assert isinstance(products, list)
    assert len(products) > 0
    assert "id" in products[0]
    assert "name" in products[0]
