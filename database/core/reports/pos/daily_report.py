class DailyPOSReport:

    def build(self, data):
        return {
            "sales": data.get("sales", 0),
            "orders": data.get("orders", 0),
            "customers": data.get("customers", 0)
        }
