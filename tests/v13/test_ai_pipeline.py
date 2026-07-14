from database.ai.pipeline.ai_pipeline import AIPipeline


def test_pipeline_creation():
    pipeline = AIPipeline()

    assert pipeline is not None
    assert pipeline.analyzer is not None
    assert pipeline.business_builder is not None
    assert pipeline.sql_planner is not None
    assert pipeline.sql_builder is not None


def test_pipeline_analyze_returns_dict():
    pipeline = AIPipeline()

    result = pipeline.analyze("show invoices")

    assert isinstance(result, dict)

    assert "analysis" in result
    assert "business_query" in result
    assert "sql_plan" in result
    assert "sql" in result
    assert "params" in result
