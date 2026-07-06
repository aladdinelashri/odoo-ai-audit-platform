class ConsoleRenderer:

    def render(self, report):

        print()

        print("=" * 70)

        print(report["title"])

        print("=" * 70)

        print()

        if not report["rows"]:

            print("No data found.")

            return

        columns = report["columns"]

        headers = []

        for column in columns:

            headers.append(column["title"])

        print(" | ".join(headers))

        print("-" * 70)

        for row in report["rows"]:

            values = []

            for column in columns:

                values.append(str(row[column["field"]]))

            print(" | ".join(values))

        print()

        print("=" * 70)

        print("Report Completed")

        print("=" * 70)
