from database.core.models import AuditResult


class CashAudit:

    def run(
        self,
        sessions
    ):

        issues = []

        for session in sessions:

            expected = session.get(
                "expected_cash",
                0
            )

            counted = session.get(
                "counted_cash",
                0
            )

            difference = (
                counted - expected
            )

            if difference != 0:

                issues.append({
                    "session": session.get("name"),
                    "expected_cash": expected,
                    "counted_cash": counted,
                    "difference": difference
                })


        return AuditResult(
            rule="cash_audit",
            status=(
                "warning"
                if issues
                else "ok"
            ),
            details={
                "count": len(issues),
                "issues": issues
            }
        )
