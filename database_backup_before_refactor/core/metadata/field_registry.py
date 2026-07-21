class FieldRegistry:

    def __init__(self):
        self.fields = {}

    def register(self, model, field):
        if model not in self.fields:
            self.fields[model] = []

        self.fields[model].append(field)

    def get(self, model):
        return self.fields.get(model, [])
