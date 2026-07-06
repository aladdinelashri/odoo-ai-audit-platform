from reporting.report_engine import ReportEngine
from locales.localization import Localization


def run():

    lang = Localization("en")

    print()

    print("==========================================")
    print(lang.text("reports.json", "products.top.title"))
    print("==========================================")

    print()

    rows = ReportEngine().top_products()

    if not rows:

        print("No data found.")
        return

    print(
        "{:<35} {:>12} {:>18}".format(
            "Product",
            "Quantity",
            "Sales"
        )
    )

    print("-" * 70)

    for row in rows:

        print(
            "{:<35} {:>12} {:>18}".format(
                str(row["product"]),
                str(row["quantity"]),
                str(row["sales"])
            )
        )

    print()

    print("==========================================")
    print(" Top Products Report Completed")
    print("==========================================")
