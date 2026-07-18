from collections import defaultdict


class ShiftAnalysis:

    def analyze(
        self,
        orders
    ):

        shifts = defaultdict(
            lambda: {
                "shift": None,
                "sales": 0,
                "orders": 0
            }
        )

        for order in orders:

            shift = order.get(
                "shift",
                "Undefined"
            )

            shifts[shift]["shift"] = shift

            shifts[shift]["sales"] += order.get(
                "amount_total",
                0
            )

            shifts[shift]["orders"] += 1


        return sorted(
            shifts.values(),
            key=lambda x: x["sales"],
            reverse=True
        )
