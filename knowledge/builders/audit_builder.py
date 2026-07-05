class AuditBuilder:

    RULES = {
        "High": [
            "Verify approvals",
            "Check audit trail",
            "Detect duplicate transactions",
            "Validate access rights",
        ],
        "Medium": [
            "Review workflow",
            "Check document completeness",
        ],
        "Low": [
            "General review",
        ],
    }

    def build(self, risk):

        return self.RULES.get(risk, ["General review"])
