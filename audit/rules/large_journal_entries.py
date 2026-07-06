from audit.rules.base_rule import AuditRule


class LargeJournalEntriesRule(AuditRule):

    id = "LARGE_JOURNAL_ENTRIES"

    def execute(self, executor):

        sql = """
        SELECT
            id,
            name,
            date,
            amount_total
        FROM account_move
        WHERE amount_total > :limit
        ORDER BY amount_total DESC
        """

        rows = executor.execute(
            sql,
            {
                "limit": 100000
            }
        )

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

            "evidence": rows[:20],

            "recommendation": metadata["recommendation"],

            "ai_prompt": metadata["ai_prompt"]

        }
