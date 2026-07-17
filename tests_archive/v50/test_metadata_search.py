from database.services.metadata_cache import MetadataCache


def test_find_company():

    cache = MetadataCache()
    cache.load()

    company = cache.find_company("جمعية مصر الجديدة")

    assert company is not None
    assert company["name"] == "جمعية مصر الجديدة"
