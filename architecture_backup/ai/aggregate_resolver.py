class AggregateResolver:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def resolve(self, intent, default_fields, detected_fields):

        if detected_fields:

            return detected_fields[0]

        numeric_priority = [

            "amount_total",
            "price_total",
            "amount_untaxed",
            "amount_tax",
            "amount_residual",
            "balance",
            "price_subtotal",
            "price_unit",
            "list_price",
            "standard_price",
            "product_qty",
            "quantity"

        ]

        for candidate in numeric_priority:

            if candidate in default_fields:

                return candidate

        if intent == "count":

            return "id"

        return "id"
