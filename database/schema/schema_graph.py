class SchemaGraph:

    def __init__(self):

        self.tables = {}

        self.edges = {}

    # ---------------------------------------------------------

    def add_table(self, table):

        if table not in self.tables:

            self.tables[table] = {}

            self.edges[table] = []

    # ---------------------------------------------------------

    def add_relation(

        self,

        source_table,

        source_field,

        target_table,

        target_field

    ):

        self.add_table(source_table)

        self.add_table(target_table)

        self.edges[source_table].append(

            {

                "source_table": source_table,

                "source_field": source_field,

                "target_table": target_table,

                "target_field": target_field

            }

        )

    # ---------------------------------------------------------

    def from_table(self, table):

        return self.edges.get(table, [])

    # ---------------------------------------------------------

    def all_tables(self):

        return list(self.tables.keys())

    # ---------------------------------------------------------

    def relation_count(self):

        return sum(

            len(v)

            for v in self.edges.values()

        )
