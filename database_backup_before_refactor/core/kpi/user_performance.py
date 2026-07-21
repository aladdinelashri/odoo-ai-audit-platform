class UserPerformance:

    def analyze(
        self,
        orders
    ):

        users = {}

        for order in orders:

            user = order.get(
                "user",
                "Undefined"
            )

            if user not in users:
                users[user] = {
                    "user": user,
                    "orders": 0,
                    "sales": 0
                }

            users[user]["orders"] += 1

            users[user]["sales"] += order.get(
                "amount_total",
                0
            )


        for item in users.values():

            item["average_order"] = (
                item["sales"] / item["orders"]
                if item["orders"]
                else 0
            )

        return sorted(
            users.values(),
            key=lambda x: x["sales"],
            reverse=True
        )
