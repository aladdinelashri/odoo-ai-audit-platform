class WhereBuilder:

    def __init__(self):

        self.conditions = []

    def add(self, field, operator, value):

        if isinstance(value, str):

            value = f"'{value}'"

        self.conditions.append(

            f"{field} {operator} {value}"

        )

    def sql(self):

        if not self.conditions:

            return ""

        return "WHERE\n    " + "\nAND ".join(self.conditions)
