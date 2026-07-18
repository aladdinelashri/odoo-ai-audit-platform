from database.core.models import AuditResult


class PaymentAudit:

    def run(
        self,
        orders
    ):

        issues = []

        for order in orders:

            order_total = order.get(
                "amount_total",
                0
            )

            paid_total = order.get(
                "paid_amount",
                0
            )

            if order_total != paid_total:

                issues.append({
                    "order": order.get("name"),
                    "order_total": order_total,
                    "paid_amount": paid_total,
                    "difference": order_total - paid_total
                })

        return AuditResult(
            rule="payment_audit",
            status=(
                "warning"
                if issues
                else "ok"
            ),
            details={
                "count": len(issues),
                "issues": issues
            }
        )
