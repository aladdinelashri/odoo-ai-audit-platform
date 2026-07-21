from database.core.models import AuditResult


class DiscountAudit:

    def run(
        self,
        orders,
        threshold=20
    ):

        high_discounts = []

        for order in orders:

            discount = order.get(
                "discount_percentage",
                0
            )

            if discount >= threshold:
                high_discounts.append({
                    "order": order.get("name"),
                    "discount_percentage": discount,
                    "user": order.get("user"),
                    "branch": order.get("branch")
                })


        status = "warning" if high_discounts else "ok"

        return AuditResult(
            rule="high_discount_transactions",
            status=status,
            details={
                "count": len(high_discounts),
                "transactions": high_discounts
            }
        )
