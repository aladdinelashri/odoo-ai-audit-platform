from database.sqlbuilder.where_builder import WhereBuilder
from database.sqlbuilder.order_builder import OrderBuilder
from database.sqlbuilder.aggregate_builder import AggregateBuilder

from database.resolver.field_resolver import FieldResolver


class SQLBuilder:

    def __init__(self):

        self.current_table = None

        self.fields = FieldResolver()

        self.selects = []

        self.joins = []

        self.aggregate = AggregateBuilder()

        self.where_builder = WhereBuilder()

        self.order_builder = OrderBuilder()

    # ---------------------------------------------------------

    def table(self, table):

        self.current_table = table

        return self

    # ---------------------------------------------------------

    def select(self, *fields):

        for field in fields:

            # -----------------------------------------
            # New Planner Style
            # -----------------------------------------

            if isinstance(field, dict):

                sql = f"{field['sql']} AS {field['alias']}"

                self.selects.append(sql)

                continue

            # -----------------------------------------
            # Old Style
            # -----------------------------------------

            item = self.fields.resolve(

                self.current_table,

                field

            )

            sql = f"{item['sql']} AS {item['alias']}"

            self.selects.append(sql)

            join = self.fields.join(

                self.current_table,

                field

            )

            if join and join not in self.joins:

                self.joins.append(join)

        return self

    # ---------------------------------------------------------

    def aggregate_from_plan(self, plan):

        sql = self.aggregate.build(plan)

        if sql:

            self.selects = [sql]

        return self

    # ---------------------------------------------------------

    def joins_from_plan(self, joins):

        for join in joins:

            if join not in self.joins:

                self.joins.append(join)

        return self

    # ---------------------------------------------------------

    def where(self, field, operator, value):

        self.where_builder.add(

            field,

            operator,

            value

        )

        return self

    # ---------------------------------------------------------

    def order_by(self, field, direction="ASC"):

        self.order_builder.add(

            field,

            direction

        )

        return self

    # ---------------------------------------------------------

    def build(self):

        sql = []

        sql.append("SELECT")

        sql.append(

            "    " +

            ",\n    ".join(self.selects)

        )

        sql.append(

            f"FROM {self.current_table}"

        )

        if self.joins:

            sql.append(

                "\n".join(self.joins)

            )

        where_sql = self.where_builder.sql()

        if where_sql:

            sql.append(where_sql)

        order_sql = self.order_builder.sql()

        if order_sql:

            sql.append(order_sql)

        return "\n".join(sql)
