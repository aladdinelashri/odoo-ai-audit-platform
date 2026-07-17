from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_query_orchestrator_creation():

    orchestrator = QueryOrchestrator()

    assert orchestrator is not None
