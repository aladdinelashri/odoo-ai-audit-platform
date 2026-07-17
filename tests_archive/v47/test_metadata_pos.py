from database.services.metadata_loader import MetadataLoader


def test_load_pos_configs():

    loader = MetadataLoader()

    pos = loader.load_pos_configs()

    assert isinstance(pos, list)

    assert len(pos) > 0

    assert "id" in pos[0]

    assert "name" in pos[0]
