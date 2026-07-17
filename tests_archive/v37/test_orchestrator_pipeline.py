from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_pipeline():

    orchestrator = QueryOrchestrator()

    result = orchestrator.run("show invoices")

    assert result == []
