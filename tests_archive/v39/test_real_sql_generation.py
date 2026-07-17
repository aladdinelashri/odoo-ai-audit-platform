from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_real_sql_generation():

    orchestrator = QueryOrchestrator()

    result = orchestrator.run("show unpaid invoices")

    assert isinstance(result, dict)
