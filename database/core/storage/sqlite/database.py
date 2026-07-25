# database/core/storage/sqlite/database.py

from pathlib import Path
from database.core.storage.sqlite.sqlite_service import SQLiteService


class SQLiteDatabase:
    """
    Backward-compatible wrapper around SQLiteService.
    All new code should use SQLiteService directly.
    This class is kept for existing audits and sync scripts.
    """

    def __init__(self, db_path=None):
        from config.settings import Settings
        self.path = db_path or Settings.SQLITE_PATH
        self._service = SQLiteService(db_path=self.path)
        self.create_schema()

    def create_schema(self):
        """Create schema if not exists."""
        self._service.execute_script(
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
            -- Session -> Business Unit Mapping
            ------------------------------------------------------------------
            CREATE TABLE IF NOT EXISTS session_business_units(
                session_id INTEGER PRIMARY KEY,
                business_unit_id INTEGER
            );
            """
        )

    def query(self, sql, params=()):
        """Execute raw SELECT query. Returns list of dicts."""
        return self._service.execute(sql, params)

    def query_one(self, sql, params=()):
        """Execute raw SQL and return first row (or None)."""
        rows = self._service.execute(sql, params)
        return rows[0] if rows else None

    def execute(self, sql, params=()):
        """Execute raw SQL (INSERT/UPDATE/DELETE). Returns cursor."""
        conn = self._service.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor

    def executemany(self, sql, rows):
        """Execute many inserts. Returns cursor."""
        return self._service.executemany(sql, rows)

    def close(self):
        """Close database connection."""
        self._service.close()
