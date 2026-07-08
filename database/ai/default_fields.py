class DefaultFields:

    def __init__(self):

        self.defaults = {

            "account_move": [

                "name",
                "date",
                "journal.name",
                "partner.name",
                "amount_total",
                "state"

            ],

            "res_partner": [

                "name",
                "phone",
                "mobile",
                "email"

            ],

            "product_product": [

                "name",
                "default_code",
                "list_price"

            ],

            "product_template": [

                "name",
                "default_code",
                "list_price"

            ],

            "pos_order": [

                "name",
                "date_order",
                "partner.name",
                "amount_total"

            ]

        }

    # ---------------------------------------------------------

    def get(self, table):

        return self.defaults.get(table, ["id"])
