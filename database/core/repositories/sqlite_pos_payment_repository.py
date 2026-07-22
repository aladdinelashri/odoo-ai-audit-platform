import sqlite3

from database.core.config import Settings


class SQLitePOSPaymentRepository:

    def __init__(self):

        settings = Settings()

        self.conn = sqlite3.connect(settings.sqlite_db_path)
        self.conn.row_factory = sqlite3.Row

    def all_payments(self):

        cursor = self.conn.execute("""
            SELECT
                id,
                order_id,
                session_id,
                payment_method,
                amount
            FROM pos_payments
            ORDER BY id
        """)

        return cursor.fetchall()

    def close(self):
        self.conn.close()
