from reporting.report_engine import ReportEngine
from locales.localization import Localization


def run():

    lang = Localization("en")

    print()

    print("===================================")
    print(lang.text("reports.json", "sales.summary.title"))
    print("===================================")

    print()

    report = ReportEngine().sales_summary()

    if not report:

        print("No data found.")
        return

    row = report[0]

    print(
        lang.text("reports.json", "sales.total_orders"),
        ":",
        row["total_orders"]
    )

    print(
        lang.text("reports.json", "sales.total_sales"),
        ":",
        row["total_sales"]
    )

    print(
        lang.text("reports.json", "sales.average_order"),
        ":",
        row["average_order"]
    )

    print()

    print("===================================")
    print(" Sales Report Completed")
    print("===================================")
