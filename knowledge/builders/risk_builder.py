class RiskBuilder:

    HIGH_RISK = [
        "account_",
        "account_move",
        "account_move_line",
        "account_payment",
        "account_bank_statement",
    ]

    MEDIUM_RISK = [
        "sale_",
        "purchase_",
        "stock_",
        "mrp_",
    ]

    def classify(self, table_name):

        for item in self.HIGH_RISK:

            if table_name.startswith(item):
                return "High"

        for item in self.MEDIUM_RISK:

            if table_name.startswith(item):
                return "Medium"

        return "Low"
