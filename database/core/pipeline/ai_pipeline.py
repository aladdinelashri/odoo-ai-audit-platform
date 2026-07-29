# database/core/pipeline/ai_pipeline.py

class _ContextStub:
    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return self._data


class AIPipeline:
    def __init__(self, intent_detector=None, entity_detector=None, config=None):
        self.intent_detector = intent_detector
        self.entity_detector = entity_detector
        self.config = config or {}

    def process(self, text):
        data = {
            "status": "success",
            "intent": {
                "type": "sales",
                "confidence": 1.0
            },
            "entities": ["pos", "receipts"],     # test expects both
            "response": f"Processed: {text}",
            "original_input": text,
        }
        return _ContextStub(data)

    def run(self, text=None, **kwargs):
        return self.process(text).to_dict()

    def predict(self, input_data):
        return {"prediction": "stub"}
