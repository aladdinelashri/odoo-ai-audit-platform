from .ai_engine import AIEngine
from .context_engine import AIContextEngine
from .explanation_engine import AIExplanationEngine
from .intent_engine import AIIntentEngine


class AIRegistry:

    def __init__(self):
        self.services = {
            "engine": AIEngine(),
            "context": AIContextEngine(),
            "explanation": AIExplanationEngine(),
            "intent": AIIntentEngine(),
        }

    def get(self, name):
        return self.services[name]
