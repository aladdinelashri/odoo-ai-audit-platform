from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_end_to_end_pipeline():

    orchestrator = QueryOrchestrator()

    queries = [
        "show invoices",
        "count invoices",
        "show unpaid invoices",
    ]

    for query in queries:
        result = orchestrator.run(query)
        assert isinstance(result, list)
