from database.resolver.relation_resolver import RelationResolver


class JoinCompiler:

    def __init__(self):

        self.resolver = RelationResolver()

    # ---------------------------------------------------------

    def compile(self, source_table, target_table):

        path = self.resolver.resolve(source_table, target_table)

        if not path:

            return []

        joins = []

        for relation in path:

            joins.append(
                f"LEFT JOIN {relation['target_table']} "
                f"ON {relation['source_table']}.{relation['source_field']} = "
                f"{relation['target_table']}.{relation['target_field']}"
            )

        return joins
