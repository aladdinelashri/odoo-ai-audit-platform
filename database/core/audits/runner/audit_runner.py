from database.core.audits.registry import AuditRegistry


class AuditRunner:

    def __init__(self):

        self.registry = AuditRegistry()

    def run(self, audit_code):

        audit = self.registry.get(audit_code)

        return audit.run()

    def run_all(self):

        results = {}

        for audit in self.registry.all():

            results[audit.code] = audit.run()

        return results
