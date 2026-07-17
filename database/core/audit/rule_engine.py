class AuditRuleEngine:

    def __init__(self):
        self.rules = []

    def register(self, rule):
        self.rules.append(rule)

    def evaluate(self, data):

        results = []

        for rule in self.rules:
            results.append(
                rule.check(data)
            )

        return results
