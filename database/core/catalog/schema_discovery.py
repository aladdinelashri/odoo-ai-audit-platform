from database.core.execution.postgres_connection import PostgresConnection


class SchemaDiscovery:

    def __init__(self):
        self.db = PostgresConnection()

    def get_tables(self):
        return self.db.fetch_all("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
            ORDER BY table_name
        """)

    def get_columns(self, table_name):
        return self.db.fetch_all(f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name='{table_name}'
            ORDER BY ordinal_position
        """)
