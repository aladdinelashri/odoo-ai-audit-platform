class IntentDetector:

    def detect(self, text: str):
        text = text.lower()

        intent = {
            "type": "unknown",
            "entities": []
        }

        if "sales" in text or "sale" in text:
            intent["type"] = "sales"

        if "invoice" in text or "receipt" in text:
            intent["type"] = "accounting"

        return intent
