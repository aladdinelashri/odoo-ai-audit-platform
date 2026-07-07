from database.schema.schema_index import SchemaIndex


class AutoJoinBuilder:

    def __init__(self):

        self.schema = SchemaIndex()

    def build(self, source_table, target_table):

        for relation in self.schema.relations_from(source_table):

            if relation["target_table"] == target_table:

                return f"""
LEFT JOIN {target_table}
ON {target_table}.{relation['target_field']} =
   {source_table}.{relation['source_field']}
""".strip()

        return None
