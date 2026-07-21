class AuditOrchestrator:

    def __init__(self, rules=None):
        self.rules = rules or []

    def add_rule(self, rule):
        self.rules.append(rule)

    def run(self, data):

        results = []

        for rule in self.rules:
            results.append(
                rule.check(data)
            )

        return results
