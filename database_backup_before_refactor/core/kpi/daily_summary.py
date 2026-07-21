from collections import defaultdict


class DailySummary:

    def summarize(
        self,
        orders
    ):

        days = defaultdict(
            lambda: {
                "date": None,
                "orders": 0,
                "sales": 0
            }
        )

        for order in orders:

            date = order.get(
                "date",
                "Undefined"
            )

            days[date]["date"] = date
            days[date]["orders"] += 1
            days[date]["sales"] += order.get(
                "amount_total",
                0
            )

        return sorted(
            days.values(),
            key=lambda x: x["date"]
        )
