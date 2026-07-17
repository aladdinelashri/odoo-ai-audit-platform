from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_orchestrator_integration():

    orchestrator = QueryOrchestrator()

    result = orchestrator.run("show unpaid invoices")

    assert isinstance(result, list)
