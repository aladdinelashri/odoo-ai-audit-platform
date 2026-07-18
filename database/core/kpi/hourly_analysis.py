from collections import defaultdict


class HourlyAnalysis:

    def analyze(
        self,
        orders
    ):

        hours = defaultdict(
            lambda: {
                "hour": None,
                "sales": 0,
                "orders": 0
            }
        )

        for order in orders:

            hour = order.get(
                "hour",
                "Undefined"
            )

            hours[hour]["hour"] = hour

            hours[hour]["sales"] += order.get(
                "amount_total",
                0
            )

            hours[hour]["orders"] += 1


        return sorted(
            hours.values(),
            key=lambda x: x["sales"],
            reverse=True
        )
