"""
Live Pipeline

Architecture V24
"""

from __future__ import annotations

from database.ai.pipeline.ai_pipeline import AIPipeline
from database.executor.query_executor import QueryExecutor
from database.results.result_formatter import ResultFormatter
from database.results.result_summary import ResultSummary


class LivePipeline:

    def __init__(
        self,
        executor: QueryExecutor,
    ) -> None:

        self.pipeline = AIPipeline()
        self.executor = executor
        self.formatter = ResultFormatter()
        self.summary = ResultSummary()

    # ---------------------------------------------------------

    def ask(self, question: str) -> dict:

        plan = self.pipeline.analyze(question)

        sql = plan["sql"]
        params = plan["params"]

        columns, rows = self.executor.execute_with_columns(
            sql,
            params,
        )

        formatted = self.formatter.format(
            columns,
            rows,
        )

        summary = self.summary.summarize(formatted)

        return {
            "question": question,
            "sql": sql,
            "params": params,
            "summary": summary,
            "columns": formatted["columns"],
            "rows": formatted["rows"],
            "count": formatted["count"],
        }
