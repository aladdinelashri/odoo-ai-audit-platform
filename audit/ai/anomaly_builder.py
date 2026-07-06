class AnomalyBuilder:

    def build(self, ai_result):

        anomalies = []

        for anomaly in ai_result.get("anomalies", []):

            anomalies.append(
                {
                    "severity": anomaly.get(
                        "severity",
                        "Medium"
                    ),
                    "description": anomaly.get(
                        "description",
                        ""
                    ),
                    "sql": anomaly.get(
                        "sql",
                        ""
                    ),
                }
            )

        return anomalies
