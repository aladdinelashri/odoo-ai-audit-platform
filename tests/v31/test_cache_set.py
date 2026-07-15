from database.cache.cache_engine import CacheEngine


def test_cache_set():

    engine = CacheEngine()

    assert engine.set("x", 1) is True
