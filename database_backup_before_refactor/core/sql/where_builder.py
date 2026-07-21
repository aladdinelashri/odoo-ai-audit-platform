class WhereBuilder:

    def build(self, filters):

        if not filters:
            return ""

        conditions = []

        for key, value in filters.items():
            conditions.append(
                f"{key} = '{value}'"
            )

        return " WHERE " + " AND ".join(conditions)
