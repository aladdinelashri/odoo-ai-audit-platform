class FilterFieldResolver:

    NUMERIC_PRIORITY = [

        "amount_total",
        "balance",
        "debit",
        "credit",
        "price_unit",
        "list_price",
        "standard_price",
        "qty",
        "quantity",
        "product_uom_qty",
        "amount_tax",
        "amount_residual"

    ]

    def resolve(self, model, detected_fields, filters):

        if not filters:
            return filters

        numeric_field = None

        for field in detected_fields:

            if field in self.NUMERIC_PRIORITY:

                numeric_field = field
                break

        if numeric_field is None:

            for field in self.NUMERIC_PRIORITY:

                if field in detected_fields:

                    numeric_field = field
                    break

        if numeric_field is None:

            if model == "account.move":

                numeric_field = "amount_total"

            elif model == "product.product":

                numeric_field = "list_price"

            elif model == "account.move.line":

                numeric_field = "balance"

        for item in filters:

            if item["field"] is None:

                item["field"] = numeric_field

        return filters
