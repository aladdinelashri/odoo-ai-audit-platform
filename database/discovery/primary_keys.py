from database.discovery.base import BaseDiscovery


class PrimaryKeyDiscovery(BaseDiscovery):

    def discover(self):

        result = {}

        for table in self.tables():

            pk = self.inspector.get_pk_constraint(table)

            result[table] = {
                "name": pk.get("name"),
                "columns": pk.get("constrained_columns", []),
            }

        return result
