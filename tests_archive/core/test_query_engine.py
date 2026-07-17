from database.core.query_engine import QueryEngine


def test_query_engine():

    engine = QueryEngine()

    result = engine.execute(
        "SELECT 1 AS value"
    )

    assert result["count"] == 1
    assert result["rows"][0]["value"] == 1
