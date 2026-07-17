from database.orchestrator.query_orchestrator import QueryOrchestrator


def test_result_type():

    orchestrator = QueryOrchestrator()

    result = orchestrator.run("show customers")

    assert result == []
