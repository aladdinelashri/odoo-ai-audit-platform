class OdooModelMapper:

    def __init__(self, model_registry):
        self.registry = model_registry

    def map_model(self, model_name, fields):
        self.registry.register(
            model_name,
            fields
        )

        return {
            "model": model_name,
            "fields": fields
        }
