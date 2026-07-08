from database.schema.schema_index import SchemaIndex
from database.resolver.table_resolver import TableResolver
from database.resolver.relation_resolver import RelationResolver
from database.jsonb.jsonb_resolver import JSONBResolver


class FieldResolver:

    def __init__(self):

        self.schema = SchemaIndex()

        self.tables = TableResolver()

        self.relations = RelationResolver()

        self.jsonb = JSONBResolver()

    # ---------------------------------------------------------

    def resolve(self, source_table, expression):

        # ---------------------------------------------
        # Local field
        # ---------------------------------------------

        if "." not in expression:

            datatype = self.schema.column_type(

                source_table,

                expression

            )

            if datatype == "jsonb":

                sql = self.jsonb.sql(

                    f"{source_table}.{expression}"

                )

            else:

                sql = f"{source_table}.{expression}"

            return {

                "sql": sql,

                "alias": expression

            }

        # ---------------------------------------------
        # Related field
        # ---------------------------------------------

        alias, field = expression.split(".", 1)

        target_table = self.tables.resolve(alias)

        if not target_table:

            raise Exception(

                f"Unknown table alias : {alias}"

            )

        datatype = self.schema.column_type(

            target_table,

            field

        )

        if datatype == "jsonb":

            sql = self.jsonb.sql(

                f"{target_table}.{field}"

            )

        else:

            sql = f"{target_table}.{field}"

        return {

            "sql": sql,

            "alias": alias

        }

    # ---------------------------------------------------------

    def join(self, source_table, expression):

        if "." not in expression:

            return None

        alias = expression.split(".", 1)[0]

        target_table = self.tables.resolve(alias)

        if not target_table:

            return None

        return self.relations.join(

            source_table,

            target_table

        )

    # ---------------------------------------------------------

    def resolve_many(self, source_table, fields):

        result = []

        joins = []

        for field in fields:

            item = self.resolve(

                source_table,

                field

            )

            result.append(item)

            join = self.join(

                source_table,

                field

            )

            if join and join not in joins:

                joins.append(join)

        return {

            "fields": result,

            "joins": joins

        }
