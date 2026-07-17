from database.reportbuilder.report_parser import ReportParser
from database.planner.planner import Planner
from database.sqlbuilder.sql_builder import SQLBuilder
from database.sql.executor import SQLExecutor


class Pipeline:

    def __init__(self):

        self.parser = ReportParser()

        self.planner = Planner()

        self.executor = SQLExecutor()

    # ---------------------------------------------------------

    def build_sql(self, report_name):

        report = self.parser.load(report_name)

        plan = self.planner.build(report)

        builder = SQLBuilder()

        builder.table(

            plan["table"]

        )

        # -----------------------------------------
        # Planner Fields
        # -----------------------------------------

        builder.select(

            *plan["select"]

        )

        # -----------------------------------------
        # Planner Joins
        # -----------------------------------------

        builder.joins_from_plan(

            plan["joins"]

        )

        # -----------------------------------------

        for item in plan["where"]:

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

        return builder.build()

    # ---------------------------------------------------------

    def execute(self, report_name):

        sql = self.build_sql(report_name)

        return self.executor.execute(sql)

    # ---------------------------------------------------------

    def explain(self, report_name):

        report = self.parser.load(report_name)

        plan = self.planner.build(report)

        sql = self.build_sql(report_name)

        return {

            "report": report_name,

            "plan": plan,

            "sql": sql

        }
