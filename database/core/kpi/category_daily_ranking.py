from collections import defaultdict


class CategoryDailyRanking:

    def rank(
        self,
        orders
    ):

        categories = defaultdict(
            lambda: {
                "category": None,
                "date": None,
                "sales": 0,
                "orders": 0
            }
        )

        for order in orders:

            category = order.get(
                "category",
                "Undefined"
            )

            date = order.get(
                "date",
                "Undefined"
            )

            key = (
                category,
                date
            )

            categories[key]["category"] = category
            categories[key]["date"] = date

            categories[key]["sales"] += order.get(
                "amount_total",
                0
            )

            categories[key]["orders"] += 1


        return sorted(
            categories.values(),
            key=lambda x: (
                x["date"],
                -x["sales"]
            )
        )
