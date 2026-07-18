from database.core.models import AuditResult


class FinancialReconciliation:

    def reconcile(
        self,
        pos_orders,
        accounting_entries
    ):

        pos_total = sum(
            order.get(
                "amount_total",
                0
            )
            for order in pos_orders
        )

        accounting_total = sum(
            entry.get(
                "amount",
                0
            )
            for entry in accounting_entries
        )

        difference = (
            pos_total - accounting_total
        )

        status = (
            "warning"
            if difference != 0
            else "ok"
        )

        return AuditResult(
            rule="pos_financial_reconciliation",
            status=status,
            details={
                "pos_total": pos_total,
                "accounting_total": accounting_total,
                "difference": difference
            }
        )
