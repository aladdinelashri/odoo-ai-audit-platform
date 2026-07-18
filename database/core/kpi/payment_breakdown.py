from collections import defaultdict


class PaymentBreakdown:

    def analyze(
        self,
        payments
    ):

        methods = defaultdict(
            lambda: {
                "method": None,
                "count": 0,
                "amount": 0
            }
        )

        for payment in payments:

            method = payment.get(
                "payment_method",
                "Undefined"
            )

            methods[method]["method"] = method

            methods[method]["count"] += 1

            methods[method]["amount"] += payment.get(
                "amount",
                0
            )


        total = sum(
            item["amount"]
            for item in methods.values()
        )

        for item in methods.values():

            item["percentage"] = (
                (item["amount"] / total) * 100
                if total
                else 0
            )


        return sorted(
            methods.values(),
            key=lambda x: x["amount"],
            reverse=True
        )
