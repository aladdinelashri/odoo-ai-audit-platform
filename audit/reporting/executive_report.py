import json
from pathlib import Path

from audit.scoring.risk_engine import RiskScoringEngine


class ExecutiveReport:

    def __init__(self):

        self.audit_report = Path(
            "audit/data/audit_report.json"
        )

        self.risk_engine = RiskScoringEngine()

    def load(self):

        with open(self.audit_report, encoding="utf-8") as f:
            return json.load(f)

    def build(self):

        report = self.load()

        risk = self.risk_engine.calculate()

        return {

            "summary": {

                "total_rules": report["total_rules"],

                "failed_rules": report["failed_rules"],

                "passed_rules": report["passed_rules"],

                "overall_score": risk["overall_score"],

                "risk_level": risk["risk_level"]

            },

            "findings": report["findings"]

        }
