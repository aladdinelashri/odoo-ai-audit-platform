from database.cache.cache_engine import CacheEngine


def test_cache_engine_creation():

    engine = CacheEngine()

    assert engine is not None
