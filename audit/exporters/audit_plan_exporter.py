import json
from pathlib import Path


class AuditPlanExporter:

    def __init__(self):

        self.output = Path("audit/data")

        self.output.mkdir(
            parents=True,
            exist_ok=True
        )

    def export(self, audit_plan):

        with open(
            self.output / "audit_plan.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                audit_plan,
                f,
                indent=4,
                ensure_ascii=False
            )

        print()

        print(f"Saved audit plan for {len(audit_plan)} tables")

        print(self.output / "audit_plan.json")
