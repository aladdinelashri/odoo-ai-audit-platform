from collections import defaultdict


class CategoryAnalysis:

    def analyze(
        self,
        orders
    ):

        categories = defaultdict(
            lambda: {
                "category": None,
                "sales": 0,
                "cost": 0,
                "profit": 0,
                "orders": 0
            }
        )

        for order in orders:

            category = order.get(
                "category",
                "Undefined"
            )

            categories[category]["category"] = category

            sales = order.get(
                "amount_total",
                0
            )

            cost = order.get(
                "cost",
                0
            )

            categories[category]["sales"] += sales

            categories[category]["cost"] += cost

            categories[category]["profit"] += sales - cost

            categories[category]["orders"] += 1


        for item in categories.values():

            item["margin_percentage"] = (
                (item["profit"] / item["sales"]) * 100
                if item["sales"]
                else 0
            )

            item["average_order"] = (
                item["sales"] / item["orders"]
                if item["orders"]
                else 0
            )


        return sorted(
            categories.values(),
            key=lambda x: x["profit"],
            reverse=True
        )
