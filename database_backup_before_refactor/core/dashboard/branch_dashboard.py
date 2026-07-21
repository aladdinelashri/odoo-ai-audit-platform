class BranchDashboard:

    def build(self, branch):
        return {
            "branch": branch.get("name"),
            "sales": branch.get("sales", 0),
            "orders": branch.get("orders", 0)
        }
