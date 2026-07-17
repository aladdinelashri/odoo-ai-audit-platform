from database.odoo.model_registry import ModelRegistry
from database.odoo.field_registry import FieldRegistry


class MetadataRegistry:

    def __init__(self):

        self.models = ModelRegistry()
        self.fields = FieldRegistry()

    # ---------------------------------------------------------

    def build(self):

        registry = {}

        for model_name in self.models.models():

            registry[model_name] = {
                "name": model_name,
                "fields": self.fields.get_fields(model_name),
            }

        return registry
