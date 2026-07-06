from pathlib import Path
import json


class HTMLExporter:

    def __init__(self):

        self.report_file = Path("audit/data/audit_report.json")

        self.template_file = Path("audit/templates/executive.html")

        self.output_file = Path("audit/reports/executive_report.html")

    def export(self):

        with open(self.report_file, encoding="utf-8") as f:
            report = json.load(f)

        with open(self.template_file, encoding="utf-8") as f:
            html = f.read()

        findings = report["findings"]

        total_score = 0

        failed_score = 0

        for finding in findings:

            total_score += finding["risk_score"]

            if finding["status"] == "FAILED":
                failed_score += finding["risk_score"]

        overall = round(failed_score / total_score * 100, 2)

        if overall >= 80:
            level = "CRITICAL"
        elif overall >= 60:
            level = "HIGH"
        elif overall >= 30:
            level = "MEDIUM"
        else:
            level = "LOW"

        rows = ""

        for finding in findings:

            css = "failed"

            if finding["status"] == "PASSED":
                css = "passed"

            rows += f"""
<tr class="{css}">
<td>{finding["title"]}</td>
<td>{finding["status"]}</td>
<td>{finding["severity"]}</td>
<td>{finding["risk_score"]}</td>
<td>{finding["records"]}</td>
</tr>
"""

        html = html.replace(
            "{{overall_score}}",
            str(overall)
        )

        html = html.replace(
            "{{risk_level}}",
            level
        )

        html = html.replace(
            "{{failed_rules}}",
            str(report["failed_rules"])
        )

        html = html.replace(
            "{{passed_rules}}",
            str(report["passed_rules"])
        )

        html = html.replace(
            "{{table_rows}}",
            rows
        )

        self.output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.output_file.write_text(
            html,
            encoding="utf-8"
        )

        print()
        print("HTML Report Saved:")
        print(self.output_file)
