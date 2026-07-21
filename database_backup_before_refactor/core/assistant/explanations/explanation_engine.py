class ExplanationEngine:

    def explain(self, audit_result):

        return {
            "rule": audit_result.rule,
            "status": audit_result.status,
            "explanation": self._generate_message(
                audit_result
            ),
            "details": audit_result.details
        }


    def _generate_message(
        self,
        audit_result
    ):

        if audit_result.status == "warning":
            return (
                "This item requires review "
                "because an audit condition was detected."
            )

        return (
            "No issues were detected "
            "for this audit rule."
        )
