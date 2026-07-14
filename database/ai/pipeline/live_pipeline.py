"""
Live Pipeline

Architecture V14

Executes the complete AI pipeline against a live PostgreSQL database.
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

        rows = self.executor.execute(sql, params)

        # For now we'll infer generic column names.
        # In the next step we'll retrieve the real names from PostgreSQL.
        columns = [f"column_{i}" for i in range(len(rows[0]))] if rows else []

        formatted = self.formatter.format(columns, rows)

        summary = self.summary.summarize(formatted)

        return {
            "question": question,
            "sql": sql,
            "params": params,
            "summary": summary,
            "rows": formatted,
        }
