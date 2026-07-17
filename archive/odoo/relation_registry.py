from database.schema.schema_index import SchemaIndex
from database.odoo.model_table_registry import ModelTableRegistry


class RelationRegistry:

    def __init__(self):

        self.schema = SchemaIndex()

        self.models = ModelTableRegistry()

        self.registry = {}

    # ---------------------------------------------------------

    def build(self):

        self.models.build()

        registry = {}

        for model, info in self.models.all().items():

            table = info["table"]

            relations = self.schema.relations_from(table)

            items = []

            for relation in relations:

                target_table = relation["target_table"]

                target_model = self.models.model(target_table)

                items.append({

                    "source_model": model,
                    "source_table": table,

                    "source_field": relation["source_field"],

                    "target_model": target_model,
                    "target_table": target_table,

                    "target_field": relation["target_field"]

                })

            registry[model] = items

        self.registry = registry

        return registry

    # ---------------------------------------------------------

    def model(self, model):

        if not self.registry:

            self.build()

        return self.registry.get(model, [])

    # ---------------------------------------------------------

    def relations(self, model):

        return self.model(model)

    # ---------------------------------------------------------

    def relation(self, model, field):

        if not self.registry:

            self.build()

        for item in self.registry.get(model, []):

            if item["source_field"] == field:

                return item

        return None

    # ---------------------------------------------------------

    def all(self):

        if not self.registry:

            self.build()

        return self.registry
