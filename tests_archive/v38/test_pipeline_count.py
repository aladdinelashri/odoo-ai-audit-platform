from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_count_query_pipeline():

    orchestrator = QueryOrchestrator()

    result = orchestrator.run("count invoices")

    assert isinstance(result, list)
