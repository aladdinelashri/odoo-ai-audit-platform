from database.v4.metadata.metadata_engine import MetadataEngine


def test_relations_return_list():

    engine = MetadataEngine()

    relations = engine.relations("account.move")

    assert isinstance(relations, list)


def test_relations_do_not_crash():

    engine = MetadataEngine()

    engine.relations("account.move")
