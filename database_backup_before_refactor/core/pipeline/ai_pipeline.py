from database.core.ai.context import AIContext


class AIPipeline:

    def __init__(self, intent_detector, entity_detector):
        self.intent_detector = intent_detector
        self.entity_detector = entity_detector

    def process(self, text):

        context = AIContext()

        intent = self.intent_detector.detect(text)
        entities = self.entity_detector.detect(text)

        context.set_intent(intent)
        context.add_entities(entities)

        return context
