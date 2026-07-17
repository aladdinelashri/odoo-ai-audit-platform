from database.odoo.metadata_registry import MetadataRegistry
from database.ai.reasoning.business_dictionary import BUSINESS_TERMS


class BusinessRegistry:

    def __init__(self):

        self.registry = self.build()

    # ---------------------------------------------------------

    def build(self):

        registry = {}

        metadata = MetadataRegistry().build()

        # -------------------------------------------------
        # Metadata aliases
        # -------------------------------------------------

        for model, info in metadata.items():

            registry[model.lower()] = model

            registry[model.replace(".", "_").lower()] = model

            name = info["name"]

            if isinstance(name, dict):

                for value in name.values():

                    if value:

                        value = str(value).strip().lower()

                        if value:

                            registry[value] = model

            elif name:

                value = str(name).strip().lower()

                if value:

                    registry[value] = model

        # -------------------------------------------------
        # Business Dictionary aliases
        # -------------------------------------------------

        for alias, model in BUSINESS_TERMS.items():

            registry[alias.strip().lower()] = model

        return registry

    # ---------------------------------------------------------

    def aliases(self):

        return self.registry

    # ---------------------------------------------------------

    def resolve(self, text):

        return self.registry.get(text.strip().lower())

    # ---------------------------------------------------------

    def exists(self, text):

        return self.resolve(text) is not None
