class AIContext:

    def __init__(self):
        self.intent = None
        self.entities = []
        self.metadata = {}

    def set_intent(self, intent):
        self.intent = intent

    def add_entities(self, entities):
        self.entities.extend(entities)

    def set_metadata(self, metadata):
        self.metadata = metadata

    def to_dict(self):
        return {
            "intent": self.intent,
            "entities": self.entities,
            "metadata": self.metadata
        }
