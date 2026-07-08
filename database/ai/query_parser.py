from database.ai.intent_detector import IntentDetector
from database.ai.entity_detector import EntityDetector
from database.ai.parameter_detector import ParameterDetector


class QueryParser:

    def __init__(self):

        self.intent = IntentDetector()

        self.entities = EntityDetector()

        self.parameters = ParameterDetector()

    # ---------------------------------------------------------

    def parse(self, text):

        intent = self.intent.detect(text)

        entities = self.entities.detect(text)

        parameters = self.parameters.detect(text)

        return {

            "text": text,

            "intent": intent,

            "entities": entities,

            "parameters": parameters

        }
