import sqlite3

from database.core.config import Settings


class SQLitePOSOrderRepository:

    def __init__(self):

        settings = Settings()

        self.conn = sqlite3.connect(settings.sqlite_db_path)
        self.conn.row_factory = sqlite3.Row

    def all_orders(self):

        cursor = self.conn.execute("""
            SELECT
                id,
                company_id,
                session_id,
                order_name,
                order_date,
                amount_total
            FROM pos_orders
            ORDER BY session_id, order_name
        """)

        return cursor.fetchall()

    def orders_by_session(self):

        cursor = self.conn.execute("""
            SELECT
                session_id,
                order_name
            FROM pos_orders
            ORDER BY session_id, order_name
        """)

        return cursor.fetchall()

    def close(self):
        self.conn.close()
