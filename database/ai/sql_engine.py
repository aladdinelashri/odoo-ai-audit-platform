from database.sqlbuilder.sql_builder import SQLBuilder


class AISQLBuilder:

    def build(self, plan):

        builder = SQLBuilder()

        builder.table(

            plan["table"]

        )

        builder.joins_from_plan(

            plan["joins"]

        )

        # -----------------------------------------
        # Aggregate
        # -----------------------------------------

        if plan.get("aggregate"):

            builder.aggregate_from_plan(

                plan

            )

        else:

            builder.select(

                *plan["fields"]

            )

        # -----------------------------------------
        # Filters
        # -----------------------------------------

        for item in plan["filters"]:

            builder.where(

                item["field"],

                item["operator"],

                item["value"]

            )

        # -----------------------------------------
        # Order
        # -----------------------------------------

        if not plan.get("aggregate"):

            for item in plan["order"]:

                builder.order_by(

                    item["field"],

                    item["direction"]

                )

        return builder.build()
