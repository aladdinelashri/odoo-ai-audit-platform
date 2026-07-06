from audit.ai.context_builder import ContextBuilder
from audit.ai.prompt_builder import PromptBuilder
from audit.ai.recommendation_builder import RecommendationBuilder
from audit.ai.anomaly_builder import AnomalyBuilder
from audit.ai.mock_ai import MockAI


class AuditAIEngine:

    def __init__(self):

        self.context_builder = ContextBuilder()
        self.prompt_builder = PromptBuilder()
        self.recommendation_builder = RecommendationBuilder()
        self.anomaly_builder = AnomalyBuilder()

        # سيتم استبداله لاحقًا بـ OpenAI أو Llama
        self.ai = MockAI()

    def analyze(self, audit_item):

        context = self.context_builder.build(audit_item)

        prompt = self.prompt_builder.build(context)

        ai_response = self.ai.analyze(prompt)

        return {

            "prompt": prompt,

            "recommendations":
                self.recommendation_builder.build(ai_response),

            "anomalies":
                self.anomaly_builder.build(ai_response),

            "raw_response":
                ai_response

        }
