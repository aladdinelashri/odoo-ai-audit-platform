class SensitiveFieldsBuilder:

    KEYWORDS = [
        "amount",
        "price",
        "balance",
        "credit",
        "debit",
        "tax",
        "payment",
        "bank",
        "currency",
        "cost",
        "salary",
        "password",
        "token",
        "secret",
        "email",
    ]

    def build(self, columns):

        sensitive = []

        for column in columns:

            name = column["name"].lower()

            for keyword in self.KEYWORDS:

                if keyword in name:
                    sensitive.append(column)
                    break

        return sensitive

    def process(self, table_name, context):

        context["sensitive_fields"] = self.build(
            context["columns"]
        )

        return context
