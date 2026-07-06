from audit.reporting.executive_report import ExecutiveReport


def run():

    print()

    print("=== Executive Audit Report ===")

    print()

    report = ExecutiveReport().build()

    summary = report["summary"]

    print("Total Rules   :", summary["total_rules"])
    print("Failed Rules  :", summary["failed_rules"])
    print("Passed Rules  :", summary["passed_rules"])

    print()

    print("Overall Score :", summary["overall_score"])
    print("Risk Level    :", summary["risk_level"])

    print()

    print("Findings")

    print("------------------------------------------------------------")

    for finding in report["findings"]:

        print(f"Rule      : {finding['rule_id']}")
        print(f"Status    : {finding['status']}")
        print(f"Severity  : {finding['severity']}")
        print(f"Risk Score: {finding['risk_score']}")
        print(f"Records   : {finding['records']}")
        print("------------------------------------------------------------")
