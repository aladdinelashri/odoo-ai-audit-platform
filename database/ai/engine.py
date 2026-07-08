from database.ai.query_parser import QueryParser
from database.planner.execution_planner import ExecutionPlanner
from database.ai.sql_engine import AISQLBuilder


class AIEngine:

    def __init__(self):

        self.parser = QueryParser()

        self.planner = ExecutionPlanner()

        self.sql = AISQLBuilder()

    # ---------------------------------------------------------

    def plan(self, text):

        parsed = self.parser.parse(text)

        return self.planner.build(parsed)

    # ---------------------------------------------------------

    def build_sql(self, text):

        plan = self.plan(text)

        return self.sql.build(plan)
