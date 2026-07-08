from database.ai.reasoning.relationships.graph import RelationshipGraph
from database.ai.reasoning.relationships.path_finder import PathFinder


class RelationResolver:

    def __init__(self):

        self.graph = RelationshipGraph()

        self.finder = PathFinder(

            self.graph

        )

    # ---------------------------------------------------------

    def relation(self, source, target):

        path = self.finder.find(

            source,

            target

        )

        if not path:

            return None

        return path[0]

    # ---------------------------------------------------------

    def exists(self, source, target):

        return self.relation(

            source,

            target

        ) is not None

    # ---------------------------------------------------------

    def join(self, source, target):

        relation = self.relation(

            source,

            target

        )

        if not relation:

            return None

        return f"""
LEFT JOIN {relation['table']}
ON {relation['table']}.{relation['target_field']} =
   {source}.{relation['source_field']}
""".strip()

    # ---------------------------------------------------------

    def path(self, source, target):

        return self.finder.find(

            source,

            target

        )
