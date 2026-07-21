class RuleRegistry:

    def __init__(self):
        self.rules = {}


    def register(
        self,
        name,
        rule
    ):

        self.rules[name] = rule


    def get(
        self,
        name
    ):

        return self.rules.get(name)


    def all(self):

        return self.rules
