from database.odoo.model_registry import ModelRegistry
from database.odoo.field_registry import FieldRegistry


class MetadataRegistry:

    def __init__(self):

        self.models = ModelRegistry()

        self.fields = FieldRegistry()

    # ---------------------------------------------------------

    def build(self):

        registry = {}

        for model in self.models.models():

            model_name = model["model"]

            registry[model_name] = {

                "name": model["name"],

                "fields": self.fields.fields(model_name)

            }

        return registry
