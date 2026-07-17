class POSAuditWidget:

    def build(
        self,
        audit_results
    ):

        warnings = [
            result.to_dict()
            for result in audit_results
            if result.status == "warning"
        ]

        return {
            "title": "POS Audit Dashboard",
            "warnings": warnings,
            "warning_count": len(warnings)
        }
