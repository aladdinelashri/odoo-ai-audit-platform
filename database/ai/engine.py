from database.ai.query_parser import QueryParser
from database.planner.execution_planner import ExecutionPlanner
from database.ai.sql_engine import AISQLBuilder

from database.sql.executor import SQLExecutor


class AIEngine:

    def __init__(self):

        self.parser = QueryParser()

        self.planner = ExecutionPlanner()

        self.sql_builder = AISQLBuilder()

        self.executor = SQLExecutor()

    # ---------------------------------------------------------

    def parse(self, text):

        return self.parser.parse(text)

    # ---------------------------------------------------------

    def plan(self, text):

        parsed = self.parse(text)

        return self.planner.build(parsed)

    # ---------------------------------------------------------

    def build_sql(self, text):

        plan = self.plan(text)

        return self.sql_builder.build(plan)

    # ---------------------------------------------------------

    def execute(self, text):

        sql = self.build_sql(text)

        return self.executor.execute(sql)

    # ---------------------------------------------------------

    def ask(self, text):

        plan = self.plan(text)

        sql = self.sql_builder.build(plan)

        result = self.executor.execute(sql)

        return {

            "question": text,

            "plan": plan,

            "sql": sql,

            "result": result

        }
