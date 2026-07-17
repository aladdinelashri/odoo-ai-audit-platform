from database.odoo.knowledge_catalog import KnowledgeCatalog
from database.odoo.field_classifier import FieldClassifier


class SemanticRegistry:

    def __init__(self):

        self.catalog = KnowledgeCatalog()

        self.classifier = FieldClassifier()

        self.registry = {}

    # ---------------------------------------------------------

    def build(self):

        self.catalog.build()

        registry = {}

        for model, info in self.catalog.all().items():

            fields = {}

            for field_name, metadata in info["fields"].items():

                fields[field_name] = {

                    "field": field_name,

                    "label": metadata["label"],

                    "type": metadata["type"],

                    "relation": metadata["relation"],

                    "semantic_role": self.classifier.classify(field_name)

                }

            registry[model] = fields

        self.registry = registry

        return registry

    # ---------------------------------------------------------

    def model(self, model):

        if not self.registry:

            self.build()

        return self.registry.get(model, {})

    # ---------------------------------------------------------

    def field(self, model, field):

        if not self.registry:

            self.build()

        return self.registry.get(model, {}).get(field)

    # ---------------------------------------------------------

    def role(self, model, field):

        item = self.field(model, field)

        if not item:

            return None

        return item["semantic_role"]

    # ---------------------------------------------------------

    def all(self):

        if not self.registry:

            self.build()

        return self.registry
