from database.v4.metadata.metadata_engine import MetadataEngine


def test_engine_cache():

    engine = MetadataEngine()

    a = engine.all_models()

    b = engine.all_models()

    assert a is b


def test_multiple_calls():

    engine = MetadataEngine()

    for _ in range(100):

        engine.fields("account.move")

        engine.statistics("account.move")

        engine.relations("account.move")
