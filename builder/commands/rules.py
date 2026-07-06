from audit.engine.rule_runner import AuditRuleRunner
from audit.reports.report_builder import AuditReportBuilder


def run():

    print()
    print("=== Audit Rule Engine ===")
    print()

    runner = AuditRuleRunner()

    report = runner.run()

    report_builder = AuditReportBuilder()

    output = report_builder.build(report)

    print(f"Total Rules  : {report['total_rules']}")
    print(f"Passed Rules : {report['passed_rules']}")
    print(f"Failed Rules : {report['failed_rules']}")

    print()

    for finding in report["findings"]:

        print(f"Rule      : {finding['rule_id']}")
        print(f"Status    : {finding['status']}")
        print(f"Records   : {finding['records']}")
        print(f"Severity  : {finding['severity']}")
        print("-" * 60)

    print()
    print(f"Audit Report Saved:")
    print(output)

    print()
    print("===================================")
    print(" Audit Rules Completed")
    print("===================================")
