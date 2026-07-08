class JoinReasoner:

    def build(self, path):

        joins = []

        if not path:

            return joins

        current_table = None

        for relation in path:

            if current_table is None:

                current_table = relation["source_field"].replace("_id", "")

            source_table = relation.get("source_table")

            if source_table is None:
                continue

            target_table = relation["table"]

            join = f"""
LEFT JOIN {target_table}
ON {target_table}.{relation['target_field']} =
   {source_table}.{relation['source_field']}
""".strip()

            joins.append(join)

        return joins
