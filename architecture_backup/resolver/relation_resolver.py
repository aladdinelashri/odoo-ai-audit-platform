from database.schema.relationship_graph import RelationshipGraph
from database.schema.path_finder import PathFinder


class RelationResolver:

    def __init__(self):

        self.graph = RelationshipGraph()

        self.finder = PathFinder(self.graph)

    # ---------------------------------------------------------

    def resolve(self, source, target):

        return self.finder.find(source, target)

    # ---------------------------------------------------------

    def relation(self, source, target):

        path = self.resolve(source, target)

        if not path:

            return None

        return path[0]

    # ---------------------------------------------------------

    def exists(self, source, target):

        return self.relation(source, target) is not None

    # ---------------------------------------------------------

    def path(self, source, target):

        return self.resolve(source, target)
