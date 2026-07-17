from database.semantic.semantic_engine import SemanticEngine


def test_concepts_is_list():

    engine = SemanticEngine()

    result = engine.analyze("show invoices")

    assert isinstance(result["concepts"], list)
