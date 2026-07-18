class BranchPOSReport:

    def build(self, data):
        return {
            "branch": data.get("branch"),
            "sales": data.get("sales", 0),
            "orders": data.get("orders", 0)
        }
