from database.schema.query_builder import QueryBuilder
from database.schema.join_builder import JoinBuilder


class SQLBuilder:

    def __init__(self):

        self.query = QueryBuilder()

        self.join_builder = JoinBuilder()

    def build(

        self,

        base_table,

        columns,

        joins=None,

        where=None,

        order=None,

        limit=None

    ):

        sql = "SELECT\n"

        sql += ",\n".join(columns)

        sql += f"\nFROM {base_table}\n"

        if joins:

            for table in joins:

                join = self.join_builder.join(

                    base_table,

                    table

                )

                if join:

                    sql += "\n"

                    sql += join

                    sql += "\n"

        if where:

            sql += "\nWHERE "

            sql += where

        if order:

            sql += "\nORDER BY "

            sql += order

        if limit:

            sql += f"\nLIMIT {limit}"

        return sql
