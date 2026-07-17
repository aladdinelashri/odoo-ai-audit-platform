import re


class FieldClassifier:

    """
    Classifies Odoo fields into business semantic roles.
    This classifier becomes the single source of truth
    for the AI engine.
    """

    def __init__(self):

        self.rules = [

            # -------------------------------------------------
            # Primary Identifier
            # -------------------------------------------------

            ("identifier", [
                r"^id$"
            ]),

            # -------------------------------------------------
            # Primary Display Name
            # -------------------------------------------------

            ("display_name", [

                r"^name$",

                r"^display_name$",

                r"^reference$",

                r"^ref$",

                r"^number$"

            ]),

            # -------------------------------------------------
            # Primary Document Date
            # -------------------------------------------------

            ("document_date", [

                r"^date$",

                r"^invoice_date$",

                r"^date_order$",

                r"^order_date$",

                r"^posting_date$"

            ]),

            # -------------------------------------------------
            # Monetary Total
            # -------------------------------------------------

            ("monetary_total", [

                r"^amount_total$",

                r"^total_amount$",

                r"^price_total$"

            ]),

            # -------------------------------------------------
            # Tax
            # -------------------------------------------------

            ("tax_amount", [

                r"^amount_tax$",

                r"^tax_amount$"

            ]),

            # -------------------------------------------------
            # Residual
            # -------------------------------------------------

            ("residual_amount", [

                r"^amount_residual$"

            ]),

            # -------------------------------------------------
            # Partner
            # -------------------------------------------------

            ("business_partner", [

                r"^partner_id$",

                r"^customer_id$",

                r"^vendor_id$"

            ]),

            # -------------------------------------------------
            # Product
            # -------------------------------------------------

            ("product", [

                r"^product_id$",

                r"^product_template_id$"

            ]),

            # -------------------------------------------------
            # Quantity
            # -------------------------------------------------

            ("quantity", [

                r"^qty$",

                r"^quantity$",

                r"^product_qty$"

            ]),

            # -------------------------------------------------
            # Unit Price
            # -------------------------------------------------

            ("price", [

                r"^price_unit$",

                r"^list_price$",

                r"^standard_price$"

            ]),

            # -------------------------------------------------
            # Status
            # -------------------------------------------------

            ("status", [

                r"^state$",

                r"^status$"

            ]),

            # -------------------------------------------------
            # Company
            # -------------------------------------------------

            ("company", [

                r"^company_id$"

            ]),

            # -------------------------------------------------
            # Journal
            # -------------------------------------------------

            ("journal", [

                r"^journal_id$"

            ]),

            # -------------------------------------------------
            # Currency
            # -------------------------------------------------

            ("currency", [

                r"^currency_id$"

            ])

        ]

    # ---------------------------------------------------------

    def classify(self, field_name):

        name = field_name.lower()

        for role, patterns in self.rules:

            for pattern in patterns:

                if re.match(pattern, name):

                    return role

        return "other"
