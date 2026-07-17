from database.services.metadata_cache import MetadataCache


def test_metadata_cache_load():

    cache = MetadataCache()

    cache.load()

    assert isinstance(cache.companies, list)

    assert len(cache.companies) > 0

    assert isinstance(cache.companies[0], dict)

    assert "id" in cache.companies[0]

    assert "name" in cache.companies[0]
