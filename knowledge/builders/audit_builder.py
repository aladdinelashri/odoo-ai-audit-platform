class AuditBuilder:

    TESTS = {
        "High": [
            "Approval workflow",
            "Duplicate detection",
            "Access control",
            "Financial reconciliation",
        ],
        "Medium": [
            "Workflow review",
            "Data integrity",
        ],
        "Low": [
            "General review",
        ],
    }

    def build(self, risk):

        return self.TESTS.get(risk, [])

    def process(self, table_name, context):

        context["audit_tests"] = self.build(
            context["risk"]
        )

        return context
