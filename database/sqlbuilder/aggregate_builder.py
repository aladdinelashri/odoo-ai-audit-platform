class AggregateBuilder:

    def build(self, plan):

        aggregate = plan.get("aggregate")

        if not aggregate:

            return None

        function = aggregate["function"]

        field = aggregate["field"]

        return f"{function}({field}) AS value"
