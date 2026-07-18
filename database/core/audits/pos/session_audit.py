from database.core.models import AuditResult


class SessionAudit:

    def run(self, sessions):

        open_sessions = [
            session
            for session in sessions
            if session.get("state") != "closed"
        ]

        status = "warning" if open_sessions else "ok"

        return AuditResult(
            rule="open_pos_sessions",
            status=status,
            details={
                "count": len(open_sessions),
                "sessions": open_sessions
            }
        )
