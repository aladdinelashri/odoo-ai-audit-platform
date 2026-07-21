from collections import defaultdict


class BranchDailyRanking:

    def rank(
        self,
        orders
    ):

        branches = defaultdict(
            lambda: {
                "branch": None,
                "date": None,
                "sales": 0,
                "orders": 0
            }
        )

        for order in orders:

            branch = order.get(
                "branch",
                "Undefined"
            )

            date = order.get(
                "date",
                "Undefined"
            )

            key = (
                branch,
                date
            )

            branches[key]["branch"] = branch
            branches[key]["date"] = date

            branches[key]["sales"] += order.get(
                "amount_total",
                0
            )

            branches[key]["orders"] += 1


        return sorted(
            branches.values(),
            key=lambda x: (
                x["date"],
                -x["sales"]
            )
        )
