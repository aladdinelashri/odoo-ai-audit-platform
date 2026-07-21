class KPIDashboard:

    def build(self, metrics):
        return {
            "sales": metrics.get("sales", 0),
            "orders": metrics.get("orders", 0),
            "profit": metrics.get("profit", 0),
        }
