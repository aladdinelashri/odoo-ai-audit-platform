from datetime import datetime


class AuditLogger:

    def __init__(self):
        self.logs = []

    def log(
        self,
        user,
        action,
        details=None
    ):

        self.logs.append({
            "timestamp": datetime.utcnow().isoformat(),
            "user": user,
            "action": action,
            "details": details or {}
        })

    def all(self):

        return self.logs
