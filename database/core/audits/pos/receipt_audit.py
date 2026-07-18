from database.core.models import AuditResult


class ReceiptAudit:

    def run(self, receipts):

        receipt_numbers = sorted(
            r.get("receipt_number")
            for r in receipts
            if r.get("receipt_number") is not None
        )

        missing = []

        for current, nxt in zip(receipt_numbers, receipt_numbers[1:]):
            if nxt > current + 1:
                missing.extend(range(current + 1, nxt))

        status = "warning" if missing else "ok"

        return AuditResult(
            rule="missing_receipt_numbers",
            status=status,
            details={
                "missing_receipts": missing,
                "checked_receipts": len(receipt_numbers)
            }
        )
