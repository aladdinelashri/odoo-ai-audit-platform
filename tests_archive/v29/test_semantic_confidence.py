from database.semantic.semantic_engine import SemanticEngine


def test_confidence_range():

    engine = SemanticEngine()

    result = engine.analyze("show invoices")

    assert 0.0 <= result["confidence"] <= 1.0
