import json
from pathlib import Path


class RiskScoringEngine:

    def __init__(self):

        self.report = Path("audit/data/audit_report.json")

    def calculate(self):

        with open(self.report, encoding="utf-8") as f:
            report = json.load(f)

        findings = report["findings"]

        total_possible = 0

        total_failed = 0

        for finding in findings:

            score = finding.get("risk_score", 0)

            total_possible += score

            if finding["status"] == "FAILED":
                total_failed += score

        overall = 0

        if total_possible:

            overall = round(
                (total_failed / total_possible) * 100,
                2
            )

        if overall >= 80:

            level = "CRITICAL"

        elif overall >= 60:

            level = "HIGH"

        elif overall >= 30:

            level = "MEDIUM"

        else:

            level = "LOW"

        return {

            "overall_score": overall,

            "risk_level": level,

            "total_possible": total_possible,

            "total_failed": total_failed

        }
