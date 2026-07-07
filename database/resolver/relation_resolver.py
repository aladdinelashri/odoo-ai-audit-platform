from database.schema.schema_index import SchemaIndex


class RelationResolver:

    def __init__(self):

        self.db = SchemaIndex()

    def from_table(self, table):

        return self.db.relations_from(table)

    def to_table(self, table):

        return self.db.relations_to(table)

    def relation(self, source, target):

        for r in self.db.relations_from(source):

            if r["target_table"] == target:

                return r

        return None

    def exists(self, source, target):

        return self.relation(source, target) is not None

    def join(self, source, target):

        rel = self.relation(source, target)

        if not rel:

            return None

        return f"""
LEFT JOIN {target}
ON {target}.{rel['target_field']} =
   {source}.{rel['source_field']}
""".strip()
