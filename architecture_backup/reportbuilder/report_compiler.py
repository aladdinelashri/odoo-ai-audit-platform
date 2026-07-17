from database.reportbuilder.report_parser import ReportParser
from database.planner.planner import Planner
from database.sqlbuilder.sql_builder import SQLBuilder


class ReportCompiler:

    def __init__(self):

        self.parser = ReportParser()

        self.planner = Planner()

    # ---------------------------------------------------------

    def compile(self, report_name):

        report = self.parser.load(report_name)

        plan = self.planner.build(report)

        builder = SQLBuilder()

        builder.table(plan["table"])

        builder.select(*plan["select"])

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
