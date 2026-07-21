class QueryBuilder:

    def build(self, intent):
        table = intent.get("table")

        if table:
            return f"SELECT * FROM {table};"

        return "SELECT 1;"
