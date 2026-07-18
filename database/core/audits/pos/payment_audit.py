from database.core.models import AuditResult


class PaymentAudit:

    def run(self, payments):

        missing_method = [
            payment
            for payment in payments
            if not payment.get("payment_method")
        ]

        status = "warning" if missing_method else "ok"

        return AuditResult(
            rule="missing_payment_method",
            status=status,
            details={
                "count": len(missing_method),
                "payments": missing_method
            }
        )
