from database.resolver.field_resolver import FieldResolver


class JoinOptimizer:

    def __init__(self):

        self.fields = FieldResolver()

    # ---------------------------------------------------------

    def optimize(self, table, fields):

        joins = []

        for field in fields:

            join = self.fields.join(

                table,

                field

            )

            if join and join not in joins:

                joins.append(join)

        return joins
