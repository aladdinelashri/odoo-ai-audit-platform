from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_real_query_planning():

    orchestrator = QueryOrchestrator()

    result = orchestrator.run("count invoices")

    assert isinstance(result, dict)
