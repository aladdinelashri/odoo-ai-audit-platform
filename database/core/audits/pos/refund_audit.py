from database.core.models import AuditResult


class RefundAudit:

    def run(self, orders):

        refunds = [
            order
            for order in orders
            if order.get("is_refund", False)
        ]

        return AuditResult(
            rule="refund_transactions",
            status="ok",
            details={
                "refund_count": len(refunds),
                "refunds": refunds
            }
        )
