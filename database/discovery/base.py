from sqlalchemy import inspect

from connectors.postgres.connection import PostgreSQLConnection


class BaseDiscovery:

    def __init__(self):

        self.engine = PostgreSQLConnection().connect()

        self.inspector = inspect(self.engine)

    def tables(self):

        return self.inspector.get_table_names()
