from ai.providers.base_provider import BaseAIProvider


class MockAIProvider(BaseAIProvider):

    def analyze(self, prompt):

        return {

            "financial_risks": [
                "High-value journal entries without approval",
                "Unusual payment timing",
            ],

            "fraud_scenarios": [
                "Duplicate vendor payments",
                "Manual journal manipulation",
            ],

            "audit_procedures": [
                "Review approval workflow",
                "Verify supporting documents",
                "Inspect access rights",
            ],

            "anomalies": [

                {
                    "severity": "High",
                    "description": "Duplicate payment reference",
                    "sql": "SELECT * FROM account_move WHERE payment_reference IS NOT NULL;"
                },

                {
                    "severity": "Medium",
                    "description": "Large manual journal entries",
                    "sql": "SELECT * FROM account_move WHERE amount_total > 100000;"
                }

            ]

        }
