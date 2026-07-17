from database.cache.cache_engine import CacheEngine


def test_cache_get_default():

    engine = CacheEngine()

    assert engine.get("missing") is None
