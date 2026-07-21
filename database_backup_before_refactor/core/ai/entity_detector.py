class EntityDetector:

    def detect(self, text: str):
        entities = []

        words = text.lower().split()

        for word in words:
            if word in ("pos", "sales", "invoice", "receipt"):
                entities.append(word)

        return entities
