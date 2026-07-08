class SemanticCatalog:

    def __init__(self):

        self.roles = {

            "account_move": {

                "monetary_total": [

                    "amount_total"

                ],

                "tax_amount": [

                    "amount_tax"

                ],

                "residual_amount": [

                    "amount_residual"

                ],

                "business_partner": [

                    "partner_id"

                ],

                "document_date": [

                    "date"

                ],

                "document_number": [

                    "name"

                ],

                "document_state": [

                    "state"

                ]

            }

        }

    # ---------------------------------------------------------

    def roles_for(self, table):

        return self.roles.get(table, {})

    # ---------------------------------------------------------

    def columns(self, table, role):

        return self.roles.get(

            table,

            {}

        ).get(

            role,

            []

        )
