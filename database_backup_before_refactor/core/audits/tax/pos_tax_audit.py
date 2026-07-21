from database.core.models import AuditResult


class POSTaxAudit:

    def run(
        self,
        orders
    ):

        issues = []

        for order in orders:

            expected_tax = order.get(
                "expected_tax",
                0
            )

            actual_tax = order.get(
                "tax_amount",
                0
            )

            if expected_tax != actual_tax:

                issues.append({
                    "order": order.get("name"),
                    "expected_tax": expected_tax,
                    "actual_tax": actual_tax,
                    "difference": expected_tax - actual_tax
                })


        status = (
            "warning"
            if issues
            else "ok"
        )

        return AuditResult(
            rule="pos_tax_audit",
            status=status,
            details={
                "count": len(issues),
                "issues": issues
            }
        )
