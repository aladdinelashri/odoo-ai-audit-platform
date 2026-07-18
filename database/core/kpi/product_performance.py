class ProductPerformance:

    def analyze(
        self,
        orders
    ):

        products = {}

        for order in orders:

            product = order.get(
                "product",
                "Undefined"
            )

            if product not in products:
                products[product] = {
                    "product": product,
                    "quantity": 0,
                    "sales": 0
                }

            products[product]["quantity"] += order.get(
                "quantity",
                0
            )

            products[product]["sales"] += order.get(
                "amount_total",
                0
            )


        return sorted(
            products.values(),
            key=lambda x: x["sales"],
            reverse=True
        )
