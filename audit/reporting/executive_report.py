import json
from pathlib import Path


class ExecutiveReport:

    def __init__(self):

        self.audit_report = Path(
            "audit/data/audit_report.json"
        )

    def load(self):

        with open(self.audit_report, encoding="utf-8") as f:
            return json.load(f)

    def build(self):

        report = self.load()

        return {

            "summary": {

                "total_rules": report["total_rules"],

                "failed_rules": report["failed_rules"],

                "passed_rules": report["passed_rules"]

            },

            "findings": report["findings"]

        }
