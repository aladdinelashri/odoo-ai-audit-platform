from database.odoo.model_table_registry import ModelTableRegistry
from database.odoo.field_registry import FieldRegistry
from database.odoo.relation_registry import RelationRegistry


class KnowledgeCatalog:

    def __init__(self):

        self.models = ModelTableRegistry()

        self.fields = FieldRegistry()

        self.relations = RelationRegistry()

        self.catalog = {}

    # ---------------------------------------------------------

    def build(self):

        self.models.build()

        self.fields.build()

        self.relations.build()

        catalog = {}

        for model, info in self.models.all().items():

            catalog[model] = {

                "model": model,

                "table": info["table"],

                "fields": self.fields.fields(model),

                "relations": self.relations.relations(model)

            }

        self.catalog = catalog

        return catalog

    # ---------------------------------------------------------

    def model(self, model):

        if not self.catalog:

            self.build()

        return self.catalog.get(model)

    # ---------------------------------------------------------

    def table(self, model):

        item = self.model(model)

        if not item:

            return None

        return item["table"]

    # ---------------------------------------------------------

    def fields_of(self, model):

        item = self.model(model)

        if not item:

            return {}

        return item["fields"]

    # ---------------------------------------------------------

    def relations_of(self, model):

        item = self.model(model)

        if not item:

            return []

        return item["relations"]

    # ---------------------------------------------------------

    def all(self):

        if not self.catalog:

            self.build()

        return self.catalog
