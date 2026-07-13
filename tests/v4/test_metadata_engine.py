from database.v4.metadata.metadata_engine import MetadataEngine


def test_metadata_engine_load():

    engine = MetadataEngine()

    assert len(engine.all_models()) > 0


def test_account_move_exists():

    engine = MetadataEngine()

    assert engine.model("account.move") is not None


def test_account_move_fields():

    engine = MetadataEngine()

    assert len(engine.fields("account.move")) > 0
