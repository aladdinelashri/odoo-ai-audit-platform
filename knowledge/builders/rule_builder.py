class RuleBuilder:

    def build(self, table_name, domain, risk):

        rules = []

        if risk == "High":

            rules.extend([
                {
                    "id": "APPROVAL",
                    "description": "Verify approval workflow"
                },
                {
                    "id": "DUPLICATE",
                    "description": "Check duplicate transactions"
                },
                {
                    "id": "ACCESS",
                    "description": "Validate user permissions"
                }
            ])

        elif risk == "Medium":

            rules.append(
                {
                    "id": "WORKFLOW",
                    "description": "Review workflow integrity"
                }
            )

        else:

            rules.append(
                {
                    "id": "GENERAL",
                    "description": "General audit review"
                }
            )

        return rules

    def process(self, table_name, context):

        context["audit_rules"] = self.build(
            table_name,
            context["domain"],
            context["risk"]
        )

        return context
