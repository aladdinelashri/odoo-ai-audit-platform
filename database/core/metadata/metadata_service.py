from database.core.execution.postgres_connection import PostgresConnection

class MetadataService:
    def __init__(self):
        self.db = PostgresConnection()

    def get_tables(self):
        return self.db.fetch_all("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
            ORDER BY table_name
        """)
