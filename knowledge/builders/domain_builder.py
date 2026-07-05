class DomainBuilder:

    DOMAIN_RULES = {
        "Accounting": [
            "account_",
        ],
        "Sales": [
            "sale_",
        ],
        "Inventory": [
            "stock_",
        ],
        "Manufacturing": [
            "mrp_",
        ],
        "Purchase": [
            "purchase_",
        ],
        "Human Resources": [
            "hr_",
        ],
        "CRM": [
            "crm_",
        ],
        "Point of Sale": [
            "pos_",
        ],
        "Website": [
            "website_",
        ],
        "Products": [
            "product_",
        ],
        "Master Data": [
            "res_",
        ],
    }

    def classify(self, table_name):

        for domain, prefixes in self.DOMAIN_RULES.items():

            for prefix in prefixes:

                if table_name.startswith(prefix):
                    return domain

        return "Other"
