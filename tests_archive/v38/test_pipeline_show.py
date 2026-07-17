from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_show_query_pipeline():

    orchestrator = QueryOrchestrator()

    result = orchestrator.run("show invoices")

    assert isinstance(result, list)
