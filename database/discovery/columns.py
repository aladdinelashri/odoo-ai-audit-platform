from database.discovery.base import BaseDiscovery


class ColumnDiscovery(BaseDiscovery):

    def discover(self):

        result = {}

        for table in self.tables():

            columns = []

            for column in self.inspector.get_columns(table):

                columns.append(
                    {
                        "name": column["name"],
                        "type": str(column["type"]),
                        "nullable": column["nullable"],
                    }
                )

            result[table] = columns

        return result
