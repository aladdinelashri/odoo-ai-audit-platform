from database.ai.pipeline.ai_pipeline import AIPipeline


def test_end_to_end_show_invoices():

    pipeline = AIPipeline()

    result = pipeline.analyze("show invoices")

    assert result["analysis"]["intent"] == "SHOW"

    assert result["business_query"].intent == "SHOW"

    assert result["sql_plan"]["from"] == "account.move"

    assert result["sql"].startswith("SELECT")

    assert isinstance(result["params"], list)
