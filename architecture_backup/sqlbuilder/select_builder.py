class SelectBuilder:

    def __init__(self):

        self.columns = []

    def add(self, *columns):

        self.columns.extend(columns)

    def sql(self):

        if not self.columns:

            return "SELECT *"

        return "SELECT\n    " + ",\n    ".join(self.columns)
