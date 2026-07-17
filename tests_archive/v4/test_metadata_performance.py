import time

from database.v4.metadata.metadata_engine import MetadataEngine


def test_metadata_speed():

    start = time.perf_counter()

    engine = MetadataEngine()

    engine.all_models()

    engine.fields("account.move")

    engine.statistics("account.move")

    engine.relations("account.move")

    elapsed = time.perf_counter() - start

    assert elapsed < 0.5
