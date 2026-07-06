import json
from pathlib import Path


class AuditReportBuilder:

    def __init__(self):

        self.output = Path(
            "audit/data/audit_report.json"
        )

    def build(self, report):

        self.output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.output,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                report,
                f,
                indent=4,
                default=str
            )

        return self.output
