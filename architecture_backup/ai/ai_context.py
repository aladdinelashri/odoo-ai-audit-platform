from database.odoo.registry import (
    metadata_service,
    business_registry,
    semantic_registry,
    relation_registry,
    knowledge_catalog,
)


class AIContext:
    """
    Shared AI context.
    """

    def __init__(self):

        self.metadata = metadata_service
        self.business = business_registry
        self.semantic = semantic_registry
        self.relations = relation_registry
        self.catalog = knowledge_catalog

        self._initialized = False

    # ---------------------------------------------------------

    def initialize(self):

        if self._initialized:
            return

        self.metadata.initialize()
        self.catalog.build()
        self.semantic.build()
        self.relations.build()

        self._initialized = True

    # ---------------------------------------------------------

    def model(self, text):

        self.initialize()
        return self.metadata.resolve_model(text)

    # ---------------------------------------------------------

    def table(self, model):

        self.initialize()
        return self.metadata.resolve_table(model)

    # ---------------------------------------------------------

    def fields(self, model):

        self.initialize()
        return self.metadata.fields(model)

    # ---------------------------------------------------------

    def relations_of(self, model):

        self.initialize()
        return self.metadata.relations_of(model)

    # ---------------------------------------------------------

    def default_fields(self, model):

        self.initialize()
        return self.metadata.default_fields(model)

    # ---------------------------------------------------------

    def semantic_role(self, model, field):

        self.initialize()
        return self.metadata.semantic_role(model, field)

    # ---------------------------------------------------------

    def exists(self, model):

        self.initialize()
        return self.metadata.exists(model)
