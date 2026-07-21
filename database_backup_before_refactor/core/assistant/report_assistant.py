from database.core.pipeline.ai_pipeline import AIPipeline
from database.core.planner.execution_planner import ExecutionPlanner
from database.core.sql.sql_builder import SQLBuilder


class ReportAssistant:

    def __init__(
        self,
        ai_pipeline,
        planner,
        sql_builder
    ):
        self.ai_pipeline = ai_pipeline
        self.planner = planner
        self.sql_builder = sql_builder


    def understand(self, question):

        context = self.ai_pipeline.process(question)

        plan = self.planner.create_plan(
            context.to_dict()
        )

        sql = self.sql_builder.build(plan)

        return {
            "context": context.to_dict(),
            "plan": plan,
            "sql": sql
        }
