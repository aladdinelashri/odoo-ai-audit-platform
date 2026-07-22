from database.core.storage.sqlite.database import SQLiteDatabase


class SQLiteSchema:

    def __init__(self):

        self.db = SQLiteDatabase()

    def create(self):

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS pos_orders(

            id INTEGER PRIMARY KEY,
            company_id INTEGER,
            session_id INTEGER,
            order_name TEXT,
            order_date TEXT,
            amount_total REAL
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS pos_payments(

            id INTEGER PRIMARY KEY,
            order_id INTEGER,
            session_id INTEGER,
            payment_method TEXT,
            amount REAL
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS pos_sessions(

            id INTEGER PRIMARY KEY,
            config_id INTEGER,
            company_id INTEGER,
            session_name TEXT,
            state TEXT,
            start_at TEXT,
            stop_at TEXT
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS pos_business_units(

            session_id INTEGER PRIMARY KEY,
            business_unit_id INTEGER,
            business_unit_name TEXT
        )
        """)
