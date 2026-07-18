from database.core.models import AuditResult


class POSAccountingAudit:

    def run(
        self,
        orders
    ):

        issues = []

        for order in orders:

            if not order.get(
                "account_move_id"
            ):

                issues.append({
                    "order": order.get("name"),
                    "issue": "missing_account_move"
                })

        status = (
            "warning"
            if issues
            else "ok"
        )

        return AuditResult(
            rule="pos_accounting_audit",
            status=status,
            details={
                "count": len(issues),
                "issues": issues
            }
        )
