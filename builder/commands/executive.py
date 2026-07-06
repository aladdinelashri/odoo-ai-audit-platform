from audit.reporting.executive_report import ExecutiveReport


def run():

    print()

    print("=== Executive Audit Report ===")

    print()

    report = ExecutiveReport().build()

    summary = report["summary"]

    print("Total Rules  :", summary["total_rules"])
    print("Failed Rules :", summary["failed_rules"])
    print("Passed Rules :", summary["passed_rules"])

    print()

    print("Findings")

    print("----------------------------------------")

    for finding in report["findings"]:

        print(finding["title"])

        print("Status    :", finding["status"])

        print("Severity  :", finding["severity"])

        print("Records   :", finding["records"])

        print("----------------------------------------")
