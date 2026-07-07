from database.reportbuilder.report_parser import ReportParser
from database.sqlbuilder.sql_builder import SQLBuilder


class ReportCompiler:

    def __init__(self):

        self.parser = ReportParser()

    # ---------------------------------------------------------

    def compile(self, report_name):

        report = self.parser.load(report_name)

        builder = SQLBuilder()

        builder.table(

            self.parser.table(report)

        )

        builder.select(

            *self.parser.fields(report)

        )

        for item in self.parser.filters(report):

            builder.where(

                item["field"],

                item["operator"],

                item["value"]

            )

        for item in self.parser.order(report):

            builder.order_by(

                item["field"],

                item["direction"]

            )

        return builder.build()
