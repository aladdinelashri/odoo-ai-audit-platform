from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_end_to_end_invoice_query():

    orchestrator = QueryOrchestrator()

    result = orchestrator.run("show invoices")

    assert isinstance(result, dict)
    assert "columns" in result
    assert "rows" in result
    assert "count" in result
