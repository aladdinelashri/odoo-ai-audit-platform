class DomainBuilder:

    DOMAINS = {
        "Accounting": [
            "account_",
        ],
        "Sales": [
            "sale_",
        ],
        "Purchase": [
            "purchase_",
        ],
        "Inventory": [
            "stock_",
        ],
        "Manufacturing": [
            "mrp_",
        ],
        "Human Resources": [
            "hr_",
        ],
        "Point of Sale": [
            "pos_",
        ],
    }

    def classify(self, table_name):

        for domain, prefixes in self.DOMAINS.items():

            for prefix in prefixes:

                if table_name.startswith(prefix):
                    return domain

        return "General"

    def process(self, table_name, context):

        context["domain"] = self.classify(table_name)

        return context
