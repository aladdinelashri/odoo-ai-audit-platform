from reporting.builders.report_builder import ReportBuilder


def run(report_name):

    builder = ReportBuilder()

    builder.build(report_name)
