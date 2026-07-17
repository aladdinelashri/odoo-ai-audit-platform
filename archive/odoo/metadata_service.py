from functools import lru_cache

from database.odoo.knowledge_catalog import KnowledgeCatalog
from database.odoo.semantic_registry import SemanticRegistry
from database.odoo.business_registry import BusinessRegistry
from database.odoo.model_table_registry import ModelTableRegistry
from database.odoo.relation_registry import RelationRegistry


class MetadataService:

    def __init__(self):

        self.knowledge = KnowledgeCatalog()

        self.semantic = SemanticRegistry()

        self.business = BusinessRegistry()

        self.models = ModelTableRegistry()

        self.relations = RelationRegistry()

        self._ready = False

    # ---------------------------------------------------------

    def initialize(self):

        if self._ready:
            return

        self.knowledge.build()

        self.semantic.build()

        self.relations.build()

        self.models.build()

        self._ready = True

    # ---------------------------------------------------------

    @lru_cache(maxsize=None)
    def resolve_model(self, text):

        self.initialize()

        return self.business.resolve(text)

    # ---------------------------------------------------------

    @lru_cache(maxsize=None)
    def resolve_table(self, model):

        self.initialize()

        return self.models.table(model)

    # ---------------------------------------------------------

    def fields(self, model):

        self.initialize()

        info = self.knowledge.model(model)

        if not info:

            return {}

        return info["fields"]

    # ---------------------------------------------------------

    def field(self, model, field):

        return self.fields(model).get(field)

    # ---------------------------------------------------------

    def semantic_role(self, model, field):

        item = self.semantic.field(model, field)

        if not item:

            return None

        return item["semantic_role"]

    # ---------------------------------------------------------

    def relations_of(self, model):

        self.initialize()

        return self.relations.model(model)

    # ---------------------------------------------------------

    def default_fields(self, model):

        """
        Return the business-default fields for a model.

        Exactly one field is selected for each semantic role.
        """

        self.initialize()

        fields = self.semantic.model(model)

        priority = [

            "display_name",

            "document_date",

            "business_partner",

            "product",

            "monetary_total",

            "tax_amount",

            "residual_amount",

            "quantity",

            "price",

            "status"

        ]

        result = []

        used = set()

        for role in priority:

            candidates = [

                field

                for field, info in fields.items()

                if info["semantic_role"] == role

            ]

            candidates.sort()

            for field in candidates:

                if field in used:

                    continue

                result.append(field)

                used.add(field)

                break

        if not result:

            return ["id"]

        return result

    # ---------------------------------------------------------

    def model_info(self, model):

        self.initialize()

        return {

            "model": model,

            "table": self.resolve_table(model),

            "fields": self.fields(model),

            "relations": self.relations_of(model),

            "default_fields": self.default_fields(model)

        }

    # ---------------------------------------------------------

    def exists(self, model):

        self.initialize()

        return self.resolve_table(model) is not None

    # ---------------------------------------------------------

    def all_models(self):

        self.initialize()

        return self.models.all()

    # ---------------------------------------------------------

    def all_relations(self):

        self.initialize()

        return self.relations.all()
