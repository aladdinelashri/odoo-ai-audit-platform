from database.core.ai.intent_detector import IntentDetector
from database.core.ai.entity_detector import EntityDetector
from database.core.pipeline.ai_pipeline import AIPipeline


def test_ai_pipeline_flow():

    pipeline = AIPipeline(
        IntentDetector(),
        EntityDetector()
    )

    context = pipeline.process(
        "show pos sales receipts"
    )

    result = context.to_dict()

    assert result["intent"]["type"] == "sales"
    assert "pos" in result["entities"]
    assert "receipts" in result["entities"]
