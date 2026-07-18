from collections import defaultdict


class MonthlySummary:

    def summarize(
        self,
        orders
    ):

        months = defaultdict(
            lambda: {
                "month": None,
                "orders": 0,
                "sales": 0,
                "refunds": 0
            }
        )

        for order in orders:

            month = order.get(
                "month",
                "Undefined"
            )

            months[month]["month"] = month

            months[month]["orders"] += 1

            amount = order.get(
                "amount_total",
                0
            )

            if order.get(
                "is_refund",
                False
            ):
                months[month]["refunds"] += amount

            else:
                months[month]["sales"] += amount


        for item in months.values():

            item["average_order"] = (
                item["sales"] / item["orders"]
                if item["orders"]
                else 0
            )

        return sorted(
            months.values(),
            key=lambda x: x["month"]
        )
