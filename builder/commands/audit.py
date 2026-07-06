from audit.builders.audit_plan_builder import AuditPlanBuilder
from audit.exporters.audit_plan_exporter import AuditPlanExporter


def run():

    print()
    print("=== Audit Plan Builder ===")
    print()

    builder = AuditPlanBuilder()
    exporter = AuditPlanExporter()

    audit_plan = builder.build()

    exporter.export(audit_plan)

    print()
    print("===================================")
    print(" Audit Plan Completed")
    print("===================================")
