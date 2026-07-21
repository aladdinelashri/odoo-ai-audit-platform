class RelationResolver:

    def resolve(self, data, relation_chain):

        current = data

        for relation in relation_chain:

            if current is None:
                return None

            value = current.get(relation)

            if value is None:
                return None

            current = value

        return current
