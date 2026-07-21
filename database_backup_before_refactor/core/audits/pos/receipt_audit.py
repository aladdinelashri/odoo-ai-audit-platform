from database.core.models import AuditResult


class ReceiptAudit:

    def run(
        self,
        receipts
    ):

        issues = []

        serials = []

        for receipt in receipts:

            serial = receipt.get(
                "serial"
            )

            if not serial:

                issues.append({
                    "receipt": receipt.get("name"),
                    "issue": "missing_serial"
                })

                continue

            if serial in serials:

                issues.append({
                    "receipt": receipt.get("name"),
                    "issue": "duplicate_serial",
                    "serial": serial
                })

            serials.append(serial)


        return AuditResult(
            rule="receipt_audit",
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
