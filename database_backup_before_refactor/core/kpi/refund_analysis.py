from collections import defaultdict


class RefundAnalysis:

    def analyze(
        self,
        orders
    ):

        summary = defaultdict(
            lambda: {
                "branch": None,
                "refund_count": 0,
                "refund_amount": 0
            }
        )

        for order in orders:

            if not order.get(
                "is_refund",
                False
            ):
                continue

            branch = order.get(
                "branch",
                "Undefined"
            )

            summary[branch]["branch"] = branch

            summary[branch]["refund_count"] += 1

            summary[branch]["refund_amount"] += order.get(
                "amount_total",
                0
            )


        return sorted(
            summary.values(),
            key=lambda x: x["refund_amount"],
            reverse=True
        )
