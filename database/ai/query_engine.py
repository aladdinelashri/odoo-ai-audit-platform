from database.ai.query_parser import QueryParser
from database.ai.execution_planner import ExecutionPlanner
from database.sqlbuilder.sql_builder import SQLBuilder


class QueryEngine:

    def __init__(self):

        self.parser = QueryParser()
        self.planner = ExecutionPlanner()

    # ---------------------------------------------------------

    def build_sql(self, text):

        parsed = self.parser.parse(text)

        plan = self.planner.build(parsed)

        builder = SQLBuilder()

        builder.table(plan["table"])

        builder.select(*plan["fields"])

        for item in plan["filters"]:

            builder.where(

                item["field"],
                item["operator"],
                item["value"]

            )

        for item in plan["order"]:

            builder.order_by(

                item["field"],
                item["direction"]

            )

        return {

            "query": text,

            "parsed": parsed,

            "plan": plan,

            "sql": builder.build()

        }
