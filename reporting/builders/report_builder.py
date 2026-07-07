import json
from pathlib import Path

from reporting.report_engine import ReportEngine
from reporting.renderers.console_renderer import ConsoleRenderer
from reporting.utils.json_formatter import JSONFormatter


class ReportBuilder:

    def __init__(self):

        self.engine = ReportEngine()

        self.renderer = ConsoleRenderer()

        self.formatter = JSONFormatter()

        self.metadata_path = Path("reporting/metadata")

    def load_metadata(self, report_name):

        file = self.metadata_path / f"{report_name}.json"

        if not file.exists():

            raise FileNotFoundError(file)

        with open(file, encoding="utf-8") as f:

            return json.load(f)

    def build(self, report_name):

        metadata = self.load_metadata(report_name)

        query = metadata["query"]

        if not hasattr(self.engine, query):

            raise Exception(f"Unknown report query: {query}")

        rows = getattr(self.engine, query)()

        rows = self.formatter.format_rows(rows)

        report = {

            "id": metadata["id"],

            "title": metadata.get("title_key", metadata["id"]),

            "columns": metadata.get("columns", []),

            "rows": rows

        }

        self.renderer.render(report)

        return report
