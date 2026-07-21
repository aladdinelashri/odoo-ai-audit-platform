from dataclasses import dataclass
from typing import Any


@dataclass
class AuditResult:
    rule: str
    status: str
    details: Any

    def to_dict(self):
        return {
            "rule": self.rule,
            "status": self.status,
            "details": self.details
        }
