class RecommendationBuilder:

    def build(self, ai_result):

        recommendations = []

        risks = ai_result.get("financial_risks", [])

        for risk in risks:

            recommendations.append(
                {
                    "priority": "High",
                    "type": "Financial Risk",
                    "recommendation": risk,
                }
            )

        frauds = ai_result.get("fraud_scenarios", [])

        for fraud in frauds:

            recommendations.append(
                {
                    "priority": "Critical",
                    "type": "Fraud",
                    "recommendation": fraud,
                }
            )

        procedures = ai_result.get("audit_procedures", [])

        for procedure in procedures:

            recommendations.append(
                {
                    "priority": "Medium",
                    "type": "Audit Procedure",
                    "recommendation": procedure,
                }
            )

        return recommendations
