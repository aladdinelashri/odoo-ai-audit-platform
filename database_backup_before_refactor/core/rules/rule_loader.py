class RuleLoader:

    def __init__(self, registry):
        self.registry = registry


    def load(self, rules):

        for rule in rules:
            self.registry.register(
                rule["name"],
                rule
            )

        return self.registry.all()
