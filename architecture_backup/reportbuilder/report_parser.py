import json
from pathlib import Path


class ReportParser:

    def __init__(self):

        self.base = Path("reporting/metadata")

    # ---------------------------------------------------------

    def load(self, report_name):

        file = self.base / f"{report_name}.json"

        if not file.exists():

            raise FileNotFoundError(file)

        with open(file, encoding="utf-8") as f:

            return json.load(f)

    # ---------------------------------------------------------

    def table(self, report):

        return report["table"]

    # ---------------------------------------------------------

    def fields(self, report):

        return report.get("fields", [])

    # ---------------------------------------------------------

    def filters(self, report):

        return report.get("filters", [])

    # ---------------------------------------------------------

    def order(self, report):

        return report.get("order_by", [])

    # ---------------------------------------------------------

    def limit(self, report):

        return report.get("limit")

    # ---------------------------------------------------------

    def title(self, report):

        return report.get("title", "")

    # ---------------------------------------------------------

    def description(self, report):

        return report.get("description", "")
