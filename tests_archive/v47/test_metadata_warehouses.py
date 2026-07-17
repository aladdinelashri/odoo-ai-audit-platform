from database.services.metadata_loader import MetadataLoader


def test_load_warehouses():

    loader = MetadataLoader()

    warehouses = loader.load_warehouses()

    assert isinstance(warehouses, list)
    assert len(warehouses) > 0
    assert "id" in warehouses[0]
    assert "name" in warehouses[0]
