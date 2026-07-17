from database.semantic.semantic_engine import SemanticEngine


def test_semantic_engine_creation():

    engine = SemanticEngine()

    assert engine is not None
