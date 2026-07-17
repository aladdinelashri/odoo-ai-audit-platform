from database.sqlbuilder.sql_builder import SQLBuilder


class AISQLBuilder:

    def build(self, plan):

        builder = SQLBuilder()

        builder.table(plan["table"])

        builder.joins_from_plan(
            plan.get("joins", [])
        )

        if plan.get("aggregate"):

            builder.aggregate_from_plan(plan)

        else:

            builder.select(
                *plan.get("fields", [])
            )

        for item in plan.get("filters", []):

            builder.where(
                item["field"],
                item["operator"],
                item["value"],
            )

        for item in plan.get(
            "order",
            plan.get("order_by", []),
        ):

            builder.order_by(
                item["field"],
                item["direction"],
            )

        if plan.get("limit") is not None:

            builder.limit(
                plan["limit"]
            )

        return builder.build()
