class SQLBuilder:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def build(self, plan):

        if not plan or not plan.get("success"):
            return None

        sql = []

        aggregate = plan.get("aggregate")

        # -------------------------------------------------
        # SELECT
        # -------------------------------------------------

        if aggregate:

            functions = {

                "count": "COUNT",

                "sum": "SUM",

                "average": "AVG",

                "min": "MIN",

                "max": "MAX"

            }

            sql_function = functions.get(

                aggregate["function"],

                aggregate["function"].upper()

            )

            sql.append(

                f"SELECT {sql_function}({aggregate['field']})"

            )

        else:

            sql.append(

                "SELECT " + ", ".join(plan["fields"])

            )

        # -------------------------------------------------
        # FROM
        # -------------------------------------------------

        sql.append(

            f"FROM {plan['table']}"

        )

        # -------------------------------------------------
        # JOIN
        # -------------------------------------------------

        for join in plan["joins"]:

            sql.append(join)

        # -------------------------------------------------
        # WHERE
        # -------------------------------------------------

        if plan["filters"]:

            where_parts = []

            for item in plan["filters"]:

                field = item["field"]

                operator = item["operator"]

                value = item["value"]

                if isinstance(value, str):

                    value = f"'{value}'"

                elif value is None:

                    value = "NULL"

                where_parts.append(

                    f"{field} {operator} {value}"

                )

            sql.append(

                "WHERE " +

                " AND ".join(where_parts)

            )

        # -------------------------------------------------
        # GROUP BY
        # -------------------------------------------------

        if plan["group_by"]:

            sql.append(

                "GROUP BY " +

                ", ".join(plan["group_by"])

            )

        # -------------------------------------------------
        # ORDER BY
        # -------------------------------------------------

        if plan["order_by"]:

            order = []

            for item in plan["order_by"]:

                direction = item.get(

                    "direction",

                    "ASC"

                )

                order.append(

                    f"{item['field']} {direction}"

                )

            sql.append(

                "ORDER BY " +

                ", ".join(order)

            )

        # -------------------------------------------------
        # LIMIT
        # -------------------------------------------------

        if plan["limit"]:

            sql.append(

                f"LIMIT {plan['limit']}"

            )

        return "\n".join(sql)
