class AggregateBuilder:

    # ---------------------------------------------------------

    def build(self, plan):

        aggregate = plan.get("aggregate")

        if not aggregate:

            return None

        function = aggregate["function"]

        field = aggregate["field"]

        parts = []

        # -------------------------------------------------
        # GROUP BY Fields
        # -------------------------------------------------

        group_fields = plan.get("group_by", [])

        for item in group_fields:

            if isinstance(item, dict):

                alias = item.get("alias", "group")

                sql = item["sql"]

                parts.append(f"{sql} AS {alias}")

            else:

                parts.append(item)

        # -------------------------------------------------
        # Aggregate
        # -------------------------------------------------

        parts.append(

            f"{function}({field}) AS value"

        )

        return ", ".join(parts)
