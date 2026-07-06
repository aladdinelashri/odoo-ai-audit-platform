import json
from pathlib import Path


class AuditPlanBuilder:

    def __init__(self):

        self.knowledge_file = Path(
            "knowledge/data/knowledge.json"
        )

    def build(self):

        with open(
            self.knowledge_file,
            "r",
            encoding="utf-8"
        ) as f:

            knowledge = json.load(f)

        audit_plan = []

        for table_name, table in knowledge.items():

            if table["risk_score"] < 60:
                continue

            audit_plan.append(
                {
                    "table": table_name,
                    "domain": table["domain"],
                    "risk": table["risk"],
                    "risk_score": table["risk_score"],
                    "audit_tests": table["audit_tests"],
                    "audit_rules": table["audit_rules"],
                    "sensitive_fields": table["sensitive_fields"],
                }
            )

        audit_plan.sort(
            key=lambda x: x["risk_score"],
            reverse=True
        )

        return audit_plan
