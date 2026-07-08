from database.resolver.field_resolver import FieldResolver


class FieldOptimizer:

    def __init__(self):

        self.fields = FieldResolver()

    # ---------------------------------------------------------

    def optimize(self, table, fields):

        result = []

        for field in fields:

            item = self.fields.resolve(

                table,

                field

            )

            result.append(item)

        return result
