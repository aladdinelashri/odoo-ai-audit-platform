class SQLBuilder:

    def build(self, query_plan):

        table = query_plan.get("table")
        fields = query_plan.get("fields", ["*"])

        if not table:
            return "SELECT 1;"

        columns = ", ".join(fields)

        return f"SELECT {columns} FROM {table};"
