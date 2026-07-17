from database.services.metadata_cache import MetadataCache


def test_metadata_cache_complete():

    cache = MetadataCache()

    cache.load()

    assert len(cache.companies) > 0
    assert len(cache.pos_configs) > 0
    assert len(cache.journals) > 0
    assert len(cache.products) > 0
    assert len(cache.partners) > 0
    assert len(cache.warehouses) > 0
