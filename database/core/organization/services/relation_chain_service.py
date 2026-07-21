class RelationChainService:

    def follow(self, obj, chain):

        current = obj

        for field in chain:

            if current is None:
                return None

            value = current.get(field)

            if value is None:
                return None

            if isinstance(value, list):
                if not value:
                    return None
                current = value[0]
            else:
                current = value

        return current
