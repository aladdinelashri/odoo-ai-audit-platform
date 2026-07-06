class RiskScoreBuilder:

    BASE_SCORE = {
        "High": 90,
        "Medium": 60,
        "Low": 20,
    }

    def calculate(self, risk, sensitive_fields):

        score = self.BASE_SCORE.get(risk, 20)

        score += len(sensitive_fields)

        if score > 100:
            score = 100

        return score

    def process(self, table_name, context):

        context["risk_score"] = self.calculate(
            context["risk"],
            context["sensitive_fields"]
        )

        return context
