from database.discovery.base import BaseDiscovery


class IndexDiscovery(BaseDiscovery):

    def discover(self):

        result = {}

        for table in self.tables():

            indexes = []

            for index in self.inspector.get_indexes(table):

                indexes.append(
                    {
                        "name": index["name"],
                        "columns": index["column_names"],
                        "unique": index["unique"],
                    }
                )

            result[table] = indexes

        return result
