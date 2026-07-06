class ContextBuilder:

    def build(self, audit_item):

        return {
            "table": audit_item["table"],
            "domain": audit_item["domain"],
            "risk": audit_item["risk"],
            "risk_score": audit_item["risk_score"],
            "risk_factor": audit_item["risk_factor"],
            "audit_tests": audit_item["audit_tests"],
            "audit_rules": audit_item["audit_rules"],
            "sensitive_fields": audit_item["sensitive_fields"],
        }
