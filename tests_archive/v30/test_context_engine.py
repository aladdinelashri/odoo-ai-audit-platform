from database.context.context_engine import ContextEngine


def test_context_engine_creation():

    engine = ContextEngine()

    assert engine is not None
