class FinancialPOSReport:

    def build(self, data):
        return {
            "gross_sales": data.get("gross_sales", 0),
            "net_sales": data.get("net_sales", 0),
            "tax": data.get("tax", 0),
            "discount": data.get("discount", 0)
        }
