class PrimaryEntityResolver:

    DOCUMENT_PRIORITY = [

        "account.move",
        "sale.order",
        "purchase.order",
        "stock.move",
        "pos.order",

    ]

    MASTER_PRIORITY = [

        "res.partner",
        "product.product",
        "product.template",

    ]

    LOOKUP_PRIORITY = [

        "account.journal",
        "res.company",
        "res.currency",

    ]

    # ---------------------------------------------------------

    def rank(self, models):

        ranked = []

        remaining = list(dict.fromkeys(models))

        for model in self.DOCUMENT_PRIORITY:

            if model in remaining:

                ranked.append(model)

                remaining.remove(model)

        for model in self.MASTER_PRIORITY:

            if model in remaining:

                ranked.append(model)

                remaining.remove(model)

        for model in self.LOOKUP_PRIORITY:

            if model in remaining:

                ranked.append(model)

                remaining.remove(model)

        ranked.extend(remaining)

        return ranked

    # ---------------------------------------------------------

    def primary(self, models):

        ranked = self.rank(models)

        if not ranked:

            return None

        return ranked[0]
