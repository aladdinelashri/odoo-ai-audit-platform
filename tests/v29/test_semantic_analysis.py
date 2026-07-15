from database.semantic.semantic_engine import SemanticEngine


def test_semantic_analysis_keys():

    engine = SemanticEngine()

    result = engine.analyze("show invoices")

    assert "text" in result
    assert "concepts" in result
    assert "confidence" in result
