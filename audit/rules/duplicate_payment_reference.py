from audit.rules.base_rule import AuditRule


class DuplicatePaymentReferenceRule(AuditRule):

    id = "DUPLICATE_PAYMENT_REFERENCE"

    def execute(self, executor):

        sql = """
        SELECT
            payment_reference,
            COUNT(*) AS duplicates
        FROM account_move
        WHERE payment_reference IS NOT NULL
        GROUP BY payment_reference
        HAVING COUNT(*) > 1
        ORDER BY duplicates DESC
        """

        rows = executor.execute(sql)

        metadata = self.metadata()

        return {

            "rule_id": metadata["id"],

            "title": metadata["title"],

            "category": metadata["category"],

            "severity": metadata["severity"],

            "risk_score": metadata["risk_score"],

            "standard": metadata["standard"],

            "description": metadata["description"],

            "status": "FAILED" if rows else "PASSED",

            "records": len(rows),

            "evidence": rows,

            "recommendation": metadata["recommendation"],

            "ai_prompt": metadata["ai_prompt"]

        }
