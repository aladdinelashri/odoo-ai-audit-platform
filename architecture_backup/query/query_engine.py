from database.ai.query_parser import QueryParser
from database.ai.execution_planner import ExecutionPlanner
from database.response.response_formatter import ResponseFormatter
from database.sql.sql_builder import SQLBuilder
from database.sql.sql_executor import SQLExecutor
from database.validator.sql_validator import SQLValidator


class QueryEngine:

    def __init__(self):

        self.parser = QueryParser()

        self.planner = ExecutionPlanner()

        self.builder = SQLBuilder()

        self.validator = SQLValidator()

        self.executor = SQLExecutor()

        self.formatter = ResponseFormatter()

    # ---------------------------------------------------------

    def execute(self, text):

        # -------------------------------------------------
        # Parse
        # -------------------------------------------------

        parsed = self.parser.parse(text)

        # -------------------------------------------------
        # Plan
        # -------------------------------------------------

        plan = self.planner.build(parsed)

        # -------------------------------------------------
        # SQL
        # -------------------------------------------------

        sql = self.builder.build(plan)

        # -------------------------------------------------
        # Validate
        # -------------------------------------------------

        self.validator.allow_tables(

            [

                plan["table"]

            ]

        )

        self.validator.validate(sql)

        # -------------------------------------------------
        # Execute
        # -------------------------------------------------

        rows = self.executor.execute(sql)

        # -------------------------------------------------
        # Format
        # -------------------------------------------------

        response = self.formatter.format(rows)

        response["plan"] = plan

        response["sql"] = sql

        return response
