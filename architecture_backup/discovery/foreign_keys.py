from database.discovery.base import BaseDiscovery


class ForeignKeyDiscovery(BaseDiscovery):

    def discover(self):

        result = {}

        for table in self.tables():

            relationships = []

            for fk in self.inspector.get_foreign_keys(table):

                relationships.append(
                    {
                        "table": table,
                        "column": fk["constrained_columns"][0]
                        if fk["constrained_columns"] else None,

                        "references_table": fk["referred_table"],

                        "references_column": fk["referred_columns"][0]
                        if fk["referred_columns"] else None,

                        "constraint": fk["name"],
                    }
                )

            result[table] = relationships

        return result
