class DataDictionary:

    def __init__(self):
        self.entries = {}


    def add(
        self,
        model,
        description
    ):

        self.entries[model] = description


    def get(
        self,
        model
    ):

        return self.entries.get(model)


    def all(self):

        return self.entries
