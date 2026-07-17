from database.core.audit.models.audit_result import AuditResult


class MissingReceiptRule:

    name = "missing_receipts"

    def check(self, receipts):

        missing = []

        for i in range(len(receipts) - 1):

            if receipts[i + 1] - receipts[i] > 1:
                missing.extend(
                    range(
                        receipts[i] + 1,
                        receipts[i + 1]
                    )
                )

        return AuditResult(
            rule=self.name,
            status="warning" if missing else "ok",
            message="Missing receipt serial numbers detected"
            if missing else "No missing receipts",
            details={
                "missing_receipts": missing
            }
        )


class RefundReviewRule:

    name = "refund_review"

    def check(self, orders):

        refunds = [
            order for order in orders
            if order.get("state") == "refund"
        ]

        return AuditResult(
            rule=self.name,
            status="warning" if refunds else "ok",
            message="Refund transactions require review"
            if refunds else "No refunds detected",
            details={
                "refund_count": len(refunds)
            }
        )
