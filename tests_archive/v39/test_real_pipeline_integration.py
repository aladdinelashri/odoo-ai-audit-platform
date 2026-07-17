from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_real_pipeline():

    orchestrator = QueryOrchestrator()

    result = orchestrator.run("show invoices")

    assert result["count"] == 0
    assert result["rows"] == []
