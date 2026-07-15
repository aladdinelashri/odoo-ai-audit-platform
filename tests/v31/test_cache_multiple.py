from database.cache.cache_engine import CacheEngine


def test_multiple_operations():

    engine = CacheEngine()

    engine.set("a", 1)
    engine.set("b", 2)

    assert engine.get("unknown") is None
