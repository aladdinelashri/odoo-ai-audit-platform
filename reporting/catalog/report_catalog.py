from pathlib import Path
import json


class ReportCatalog:

    def __init__(self):

        self.path = Path("reporting/metadata")

    def load(self):

        reports = []

        if not self.path.exists():
            return reports

        for file in sorted(self.path.glob("*.json")):

            with open(file, encoding="utf-8") as f:

                reports.append(json.load(f))

        return reports

    def count(self):

        return len(self.load())
