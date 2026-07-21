class ModelRegistry:

    def __init__(self):
        self.models = {}


    def register(
        self,
        model_name,
        metadata
    ):

        self.models[model_name] = metadata


    def get(self, model_name):

        return self.models.get(
            model_name
        )


    def all(self):

        return self.models
