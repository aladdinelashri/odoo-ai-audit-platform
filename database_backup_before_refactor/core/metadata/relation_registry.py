class RelationRegistry:

    def __init__(self):
        self.relations = []

    def register(self, relation):
        self.relations.append(relation)

    def get_all(self):
        return self.relations
