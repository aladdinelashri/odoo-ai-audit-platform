class ValidationBuilder:

    REQUIRED = [
        "columns",
        "primary_key",
        "foreign_keys",
        "indexes",
        "constraints",
    ]

    def process(self, table_name, context):

        missing = []

        for field in self.REQUIRED:

            if field not in context:
                missing.append(field)

        context["validation"] = {
            "valid": len(missing) == 0,
            "missing": missing,
        }

        return context
