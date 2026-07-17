class AuditSchema:

    def __init__(self):

        self.tables = {}


    def register_table(
        self,
        name,
        fields
    ):

        self.tables[name] = fields


    def get_table(
        self,
        name
    ):

        return self.tables.get(name)


    def all_tables(self):

        return self.tables
