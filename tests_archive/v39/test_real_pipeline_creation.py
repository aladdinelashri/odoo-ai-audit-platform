from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_real_pipeline_creation():

    orchestrator = QueryOrchestrator()

    assert orchestrator is not None
