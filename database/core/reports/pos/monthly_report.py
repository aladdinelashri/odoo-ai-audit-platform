class MonthlyPOSReport:

    def build(self, data):
        return {
            "sales": data.get("sales", 0),
            "orders": data.get("orders", 0),
            "average_ticket": data.get("average_ticket", 0)
        }
