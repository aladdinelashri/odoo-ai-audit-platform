class CategoryComparison:

    def compare(
        self,
        orders
    ):

        categories = {}

        for order in orders:

            category = order.get(
                "category",
                "Undefined"
            )

            if category not in categories:
                categories[category] = {
                    "category": category,
                    "sales": 0,
                    "orders": 0
                }

            categories[category]["sales"] += order.get(
                "amount_total",
                0
            )

            categories[category]["orders"] += 1


        for item in categories.values():

            item["average_order"] = (
                item["sales"] / item["orders"]
                if item["orders"]
                else 0
            )

        return sorted(
            categories.values(),
            key=lambda x: x["sales"],
            reverse=True
        )
