# database/core/storage/sqlite/database.py

from pathlib import Path
import sqlite3


class SQLiteDatabase:

    def __init__(self):

        root = Path(__file__).resolve().parents[4]

        db_folder = root / "database" / "storage"
        db_folder.mkdir(parents=True, exist_ok=True)

        self.path = db_folder / "audit.db"

        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row

        self.create_schema()

    def create_schema(self):

        cursor = self.connection.cursor()

        cursor.executescript(
            """
            ------------------------------------------------------------------
            -- POS Orders
            ------------------------------------------------------------------
            CREATE TABLE IF NOT EXISTS pos_orders(
                id INTEGER PRIMARY KEY,
                company_id INTEGER,
                session_id INTEGER,
                partner_id INTEGER,
                state TEXT,
                order_name TEXT,
                order_date TEXT,
                amount_total REAL
            );

            ------------------------------------------------------------------
            -- POS Order Lines
            ------------------------------------------------------------------
            CREATE TABLE IF NOT EXISTS pos_order_lines(
                id INTEGER PRIMARY KEY,
                order_id INTEGER,
                product_id INTEGER,
                qty REAL,
                price_subtotal REAL
            );

            ------------------------------------------------------------------
            -- Product Products
            ------------------------------------------------------------------
            CREATE TABLE IF NOT EXISTS product_products(
                id INTEGER PRIMARY KEY,
                display_name TEXT,
                categ_id INTEGER,
                categ_name TEXT
            );

            ------------------------------------------------------------------
            -- POS Payments
            ------------------------------------------------------------------
            CREATE TABLE IF NOT EXISTS pos_payments(
                id INTEGER PRIMARY KEY,
                order_id INTEGER,
                session_id INTEGER,
                payment_method TEXT,
                amount REAL
            );

            ------------------------------------------------------------------
            -- POS Sessions
            ------------------------------------------------------------------
            CREATE TABLE IF NOT EXISTS pos_sessions(
                id INTEGER PRIMARY KEY,
                config_id INTEGER,
                session_name TEXT
            );

            ------------------------------------------------------------------
            -- POS Configs
            ------------------------------------------------------------------
            CREATE TABLE IF NOT EXISTS pos_configs(
                id INTEGER PRIMARY KEY,
                company_id INTEGER,
                name TEXT,
                iface_available_categ_ids TEXT
            );

            ------------------------------------------------------------------
            -- Business Units
            ------------------------------------------------------------------
            CREATE TABLE IF NOT EXISTS business_units(
                id INTEGER PRIMARY KEY,
                code TEXT,
                name TEXT,
                source TEXT
            );

            ------------------------------------------------------------------
            -- Session → Business Unit Mapping
            ------------------------------------------------------------------
            CREATE TABLE IF NOT EXISTS session_business_units(
                session_id INTEGER PRIMARY KEY,
                business_unit_id INTEGER
            );
            """
        )

        self.connection.commit()

    def execute(self, sql, params=()):

        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        self.connection.commit()
        return cursor

    def executemany(self, sql, rows):

        cursor = self.connection.cursor()
        cursor.executemany(sql, rows)
        self.connection.commit()
        return cursor

    def query(self, sql, params=()):

        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

    def query_one(self, sql, params=()):

        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchone()

    def close(self):

        self.connection.close()
