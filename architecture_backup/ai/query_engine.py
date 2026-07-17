from database.planner.execution_planner import ExecutionPlanner
from database.sql.sql_builder import SQLBuilder


class QueryEngine:

    def __init__(self):

        self.planner = ExecutionPlanner()

        self.sql = SQLBuilder()

    # ---------------------------------------------------------

    def execute(self, question):

        plan = self.planner.build(question)

        if not plan.get("success"):

            return plan

        sql = self.sql.build(plan)

        return {

            "success": True,

            "question": question,

            "plan": plan,

            "sql": sql

        }
