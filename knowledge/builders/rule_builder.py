class RuleBuilder:

    def build(self, table_name, domain, risk):

        rules = []

        if risk == "High":

            rules.append(
                {
                    "id": "APPROVAL",
                    "description": "Verify approval workflow"
                }
            )

            rules.append(
                {
                    "id": "DUPLICATE",
                    "description": "Check duplicate transactions"
                }
            )

            rules.append(
                {
                    "id": "ACCESS",
                    "description": "Validate user permissions"
                }
            )

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
