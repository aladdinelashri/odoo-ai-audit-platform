from database.core.models import AuditResult


class SessionAudit:

    def run(
        self,
        sessions
    ):

        issues = []

        for session in sessions:

            if not session.get(
                "closed",
                False
            ):

                issues.append({
                    "session": session.get("name"),
                    "issue": "unclosed_session"
                })


        return AuditResult(
            rule="session_audit",
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
