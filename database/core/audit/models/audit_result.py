class AuditResult:

    def __init__(
        self,
        rule,
        status,
        message,
        details=None
    ):
        self.rule = rule
        self.status = status
        self.message = message
        self.details = details or {}

    def to_dict(self):

        return {
            "rule": self.rule,
            "status": self.status,
            "message": self.message,
            "details": self.details
        }
