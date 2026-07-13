from database.v4.metadata.metadata_engine import MetadataEngine


def test_statistics_return_dict():

    engine = MetadataEngine()

    stats = engine.statistics("account.move")

    assert isinstance(stats, dict)


def test_statistics_do_not_crash():

    engine = MetadataEngine()

    engine.statistics("account.move")
