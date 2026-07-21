from database.core.models import AuditResult


class POSAnomalyDetector:

    def detect(
        self,
        orders,
        threshold=2
    ):

        anomalies = []

        for order in orders:

            amount = order.get(
                "amount_total",
                0
            )

            if amount >= threshold:
                anomalies.append({
                    "order": order.get("name"),
                    "amount": amount,
                    "reason": "high_value_order"
                })

        status = "warning" if anomalies else "ok"

        return AuditResult(
            rule="pos_anomaly_detection",
            status=status,
            details={
                "count": len(anomalies),
                "anomalies": anomalies
            }
        )
