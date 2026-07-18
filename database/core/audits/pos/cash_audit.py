from database.core.models import AuditResult


class CashAudit:

    def run(self, sessions):

        mismatches = []

        for session in sessions:
            expected = session.get("expected_cash", 0)
            counted = session.get("counted_cash", 0)

            if expected != counted:
                mismatches.append({
                    "session": session.get("name"),
                    "expected_cash": expected,
                    "counted_cash": counted,
                    "difference": counted - expected
                })

        status = "warning" if mismatches else "ok"

        return AuditResult(
            rule="cash_mismatch",
            status=status,
            details={
                "count": len(mismatches),
                "mismatches": mismatches
            }
        )
