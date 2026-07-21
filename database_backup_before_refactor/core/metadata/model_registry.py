class ModelRegistry:

    def __init__(self):
        self.models = {}

    def register(self, name, fields=None):
        self.models[name] = fields or []

    def get(self, name):
        return self.models.get(name)
