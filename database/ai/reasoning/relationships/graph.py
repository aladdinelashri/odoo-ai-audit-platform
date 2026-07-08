class RelationshipGraph:

    def __init__(self):

        self.graph = {}

    # ---------------------------------------------------------

    def add(self, source, target):

        self.graph.setdefault(

            source,

            []

        ).append(target)

    # ---------------------------------------------------------

    def neighbors(self, table):

        return self.graph.get(

            table,

            []

        )
