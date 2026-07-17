from database.odoo.business_registry import BusinessRegistry
from database.schema.schema_index import SchemaIndex


class EntityRegistry:

    def __init__(self):

        self.schema = SchemaIndex()

        self.registry = {}

        aliases = BusinessRegistry().aliases()

        for alias, model in aliases.items():

            table = model.replace(".", "_")

            if self.schema.exists(table):

                self.registry[alias] = table

            else:

                self.registry[alias] = model

    # ---------------------------------------------------------

    def resolve(self, text):

        lowered = text.strip().lower()

        return self.registry.get(lowered)

    # ---------------------------------------------------------

    def exists(self, text):

        return self.resolve(text) is not None

    # ---------------------------------------------------------

    def all(self):

        return self.registry
