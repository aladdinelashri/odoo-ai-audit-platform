class RuleEngine:

    def __init__(self, registry):
        self.registry = registry


    def evaluate(self, data):

        results = []

        for name, rule in self.registry.all().items():

            evaluator = rule.get("evaluator")

            if callable(evaluator):
                results.append(
                    evaluator(data)
                )

        return results
