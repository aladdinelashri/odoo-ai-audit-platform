class BranchComparison:

    def compare(
        self,
        branches
    ):

        result = []

        for branch in branches:
            result.append({
                "branch": branch.get("name"),
                "sales": branch.get("sales", 0),
                "orders": branch.get("orders", 0)
            })

        return sorted(
            result,
            key=lambda x: x["sales"],
            reverse=True
        )
