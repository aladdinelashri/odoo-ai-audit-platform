from collections import defaultdict


class ProfitabilityAnalysis:

    def analyze(
        self,
        orders
    ):

        products = defaultdict(
            lambda: {
                "product": None,
                "sales": 0,
                "cost": 0,
                "profit": 0
            }
        )

        for order in orders:

            product = order.get(
                "product",
                "Undefined"
            )

            products[product]["product"] = product

            sales = order.get(
                "amount_total",
                0
            )

            cost = order.get(
                "cost",
                0
            )

            products[product]["sales"] += sales
            products[product]["cost"] += cost
            products[product]["profit"] += sales - cost


        for item in products.values():

            item["margin_percentage"] = (
                (item["profit"] / item["sales"]) * 100
                if item["sales"]
                else 0
            )

        return sorted(
            products.values(),
            key=lambda x: x["profit"],
            reverse=True
        )
