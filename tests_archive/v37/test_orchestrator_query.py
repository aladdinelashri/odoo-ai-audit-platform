from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_query_input():

    orchestrator = QueryOrchestrator()

    result = orchestrator.run("count invoices")

    assert isinstance(result, list)
