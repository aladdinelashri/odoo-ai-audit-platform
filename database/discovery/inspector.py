from sqlalchemy import inspect

from connectors.postgres.connection import PostgreSQLConnection


class SchemaInspector:

    def __init__(self):

        self.connection = PostgreSQLConnection()

    def get_tables(self):

        engine = self.connection.connect()

        inspector = inspect(engine)

        return sorted(inspector.get_table_names())
