from database.catalog.semantic_catalog import SemanticCatalog


class FieldRanker:

    def __init__(self):

        self.semantic = SemanticCatalog()

    # ---------------------------------------------------------

    def best(self, table, role):

        columns = self.semantic.columns(

            table,

            role

        )

        if not columns:

            return None

        return columns[0]

    # ---------------------------------------------------------

    def all(self, table, role):

        return self.semantic.columns(

            table,

            role

        )
