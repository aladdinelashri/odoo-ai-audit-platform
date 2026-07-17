from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_filtered_query_pipeline():

    orchestrator = QueryOrchestrator()

    result = orchestrator.run("show unpaid invoices")

    assert isinstance(result, list)
