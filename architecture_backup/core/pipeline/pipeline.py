"""
Core Pipeline

Architecture V3

Query
    ↓
Query Parser
    ↓
Execution Planner
    ↓
SQL Builder
    ↓
SQL Validator
    ↓
SQL Executor
    ↓
Response Formatter
"""

from __future__ import annotations

from database.core.pipeline.context import PipelineContext
from database.core.pipeline.result import PipelineResult

from database.core.ai.query_parser import QueryParser
from database.core.planner.execution_planner import ExecutionPlanner
from database.core.sql.sql_builder import SQLBuilder
from database.core.security.sql_validator import SQLValidator
from database.core.sql.sql_executor import SQLExecutor
from database.core.response.response_formatter import ResponseFormatter


class Pipeline:
    """
    Architecture V3 Core Pipeline.
    """

    def __init__(self) -> None:

        self.parser = QueryParser()
        self.planner = ExecutionPlanner()
        self.builder = SQLBuilder()
        self.validator = SQLValidator()
        self.executor = SQLExecutor()
        self.formatter = ResponseFormatter()

    # ---------------------------------------------------------

    def execute(self, query: str) -> PipelineResult:
        """
        Execute one complete pipeline.
        """

        context = PipelineContext(query=query)

        try:

            # ------------------------------------------
            # Parse
            # ------------------------------------------

            context.parsed = self.parser.parse(context)

            # ------------------------------------------
            # Planning
            # ------------------------------------------

            context.execution_plan = self.planner.build(context)

            # ------------------------------------------
            # SQL Generation
            # ------------------------------------------

            context.sql = self.builder.build(context)

            # ------------------------------------------
            # Validation
            # ------------------------------------------

            self.validator.validate(context)

            # ------------------------------------------
            # Execute
            # ------------------------------------------

            context.rows = self.executor.execute(context)

            # ------------------------------------------
            # Format Response
            # ------------------------------------------

            context.response = self.formatter.format(context)

            return PipelineResult(**context.response)

        except Exception as exc:

            context.fail(str(exc))

            return PipelineResult(
                success=False,
                count=0,
                rows=[],
                value=None,
                error=str(exc),
            )

    # ---------------------------------------------------------

    def run(self, query: str) -> dict:
        """
        Compatibility API used by V4 tests.
        """

        result = self.execute(query)

        response = result.to_dict()

        # Compatibility field required by tests
        response["sql"] = None

        return response
