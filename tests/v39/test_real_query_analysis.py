from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_real_query_analysis():

    orchestrator = QueryOrchestrator()

    result = orchestrator.run("show invoices")

    assert isinstance(result, dict)
