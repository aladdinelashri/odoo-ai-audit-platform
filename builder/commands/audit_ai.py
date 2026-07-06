import json

from audit.ai.engine import AuditAIEngine


def run():

    print()
    print("=== Audit AI Engine ===")
    print()

    with open(
        "audit/data/audit_plan.json",
        "r",
        encoding="utf-8"
    ) as f:

        audit_plan = json.load(f)

    engine = AuditAIEngine()

    result = engine.analyze(
        audit_plan[0]
    )

    print("Table:")
    print(audit_plan[0]["table"])

    print()
    print("Recommendations:")

    for item in result["recommendations"]:

        print("-", item["recommendation"])

    print()
    print("Anomalies:")

    for item in result["anomalies"]:

        print("-", item["description"])
