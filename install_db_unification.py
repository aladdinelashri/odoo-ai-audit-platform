#!/usr/bin/env python3
"""
Install DB Interface Unification Script
Backs up old files, installs new ones, runs tests.
"""
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path("/home/helioit/odoo-ai-audit-platform")

FILES = {
    "sqlite_service.py": {
        "target": PROJECT_ROOT / "database/core/storage/sqlite/sqlite_service.py",
        "content": '''"""
SQLite Service -- query builder and executor with full operator support.
Unified interface for all database operations.
"""
import sqlite3
import logging
from typing import List, Tuple, Any, Optional, Dict, Union
from pathlib import Path

from config.logging import get_logger

logger = get_logger('database.sqlite')


# -- Field Mapping: Odoo names -> SQLite columns --
FIELD_MAP: Dict[str, str] = {
    # POS Orders
    'name': 'order_name',
    'date_order': 'order_date',
    'amount_total': 'amount_total',
    'amount_paid': 'amount_paid',
    'amount_return': 'amount_return',
    'state': 'state',
    'partner_id': 'partner_id',
    'user_id': 'user_id',
    'session_id': 'session_id',
    'pos_reference': 'pos_reference',

    # POS Payments
    'payment_method_id': 'payment_method_id',
    'amount': 'amount',
    'payment_date': 'payment_date',

    # POS Sessions
    'start_at': 'start_at',
    'stop_at': 'stop_at',
    'config_id': 'config_id',

    # Products
    'product_id': 'product_id',
    'qty': 'quantity',
    'price_unit': 'price_unit',

    # Business Units
    'business_unit_id': 'business_unit_id',
    'company_id': 'company_id',
}


# -- Operators --
OPERATORS: Dict[str, Any] = {
    '=':  lambda col, val: (f"{col} = ?", [val]),
    '!=': lambda col, val: (f"{col} != ?", [val]),
    '<':  lambda col, val: (f"{col} < ?", [val]),
    '>':  lambda col, val: (f"{col} > ?", [val]),
    '<=': lambda col, val: (f"{col} <= ?", [val]),
    '>=': lambda col, val: (f"{col} >= ?", [val]),
    'like': lambda col, val: (f"{col} LIKE ?", [f"%{val}%"]),
    'in': lambda col, val: (f"{col} IN ({','.join('?' * len(val))})", list(val) if isinstance(val, (list, tuple)) else [val]),
    'between': lambda col, val: (f"{col} BETWEEN ? AND ?", list(val) if isinstance(val, (list, tuple)) else [val, val]),
}


class SQLiteService:
    """High-level SQLite query service -- unified interface for all DB operations."""

    def __init__(self, db_path: str = None):
        from config.settings import Settings
        self.db_path = db_path or Settings.SQLITE_PATH
        self.conn = None

    def connect(self):
        """Establish database connection."""
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            logger.debug(f"Connected to SQLite: {self.db_path}")
        return self.conn

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def _resolve_field(self, field: str) -> str:
        """Map Odoo field name to SQLite column name."""
        return FIELD_MAP.get(field, field)

    def _build_where(self, conditions: List[Tuple]) -> Tuple[str, List[Any]]:
        """Build WHERE clause from conditions."""
        if not conditions:
            return "", []

        clauses = []
        params = []

        for condition in conditions:
            if len(condition) != 3:
                logger.warning(f"Invalid condition: {condition}")
                continue

            field, op, value = condition
            col = self._resolve_field(field)

            if op not in OPERATORS:
                logger.warning(f"Unsupported operator '{op}', using '='")
                op = '='

            clause, p = OPERATORS[op](col, value)
            clauses.append(clause)
            params.extend(p)

        if not clauses:
            return "", []

        where = " WHERE " + " AND ".join(clauses)
        return where, params

    def query(
        self,
        table: str,
        columns: List[str] = None,
        conditions: List[Tuple] = None,
        order_by: str = None,
        limit: int = None,
        offset: int = None
    ) -> List[Dict[str, Any]]:
        """Execute a SELECT query with full operator support."""
        conn = self.connect()
        cursor = conn.cursor()

        cols = ", ".join(columns) if columns else "*"
        sql = f"SELECT {cols} FROM {table}"

        where, params = self._build_where(conditions or [])
        sql += where

        if order_by:
            sql += f" ORDER BY {self._resolve_field(order_by)}"
        if limit:
            sql += f" LIMIT {limit}"
        if offset:
            sql += f" OFFSET {offset}"

        logger.debug(f"SQL: {sql} | Params: {params}")

        try:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Query failed: {sql} | Error: {e}")
            raise

    def search(
        self,
        table: str,
        domain: List[Tuple] = None,
        fields: List[str] = None,
        limit: int = None,
        order: str = None
    ) -> List[Dict[str, Any]]:
        """
        Search records matching a domain (Odoo-style).
        Alias for query() with domain as conditions.
        """
        return self.query(
            table=table,
            columns=fields,
            conditions=domain,
            limit=limit,
            order_by=order,
        )

    def read(
        self,
        table: str,
        ids: Union[int, List[int]],
        fields: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Read records by ID(s)."""
        if not ids:
            return []
        if isinstance(ids, int):
            ids = [ids]
        return self.query(
            table=table,
            columns=fields,
            conditions=[("id", "in", ids)],
        )

    def count(self, table: str, conditions: List[Tuple] = None) -> int:
        """Count rows matching conditions."""
        conn = self.connect()
        cursor = conn.cursor()

        sql = f"SELECT COUNT(*) FROM {table}"
        where, params = self._build_where(conditions or [])
        sql += where

        cursor.execute(sql, params)
        return cursor.fetchone()[0]

    def sum(self, table: str, column: str, conditions: List[Tuple] = None) -> float:
        """Sum a column matching conditions."""
        conn = self.connect()
        cursor = conn.cursor()

        col = self._resolve_field(column)
        sql = f"SELECT COALESCE(SUM({col}), 0) FROM {table}"
        where, params = self._build_where(conditions or [])
        sql += where

        cursor.execute(sql, params)
        result = cursor.fetchone()[0]
        return float(result) if result else 0.0

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """Insert a row and return lastrowid."""
        conn = self.connect()
        cursor = conn.cursor()

        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor.execute(sql, list(data.values()))
        conn.commit()
        return cursor.lastrowid

    def insert_many(self, table: str, rows: List[Dict[str, Any]]) -> int:
        """Insert multiple rows."""
        if not rows:
            return 0

        conn = self.connect()
        cursor = conn.cursor()

        columns = ", ".join(rows[0].keys())
        placeholders = ", ".join("?" * len(rows[0]))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        values = [list(row.values()) for row in rows]
        cursor.executemany(sql, values)
        conn.commit()
        return cursor.rowcount

    def executemany(self, sql: str, rows: List[Any]) -> int:
        """Execute raw SQL for multiple rows."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executemany(sql, rows)
        conn.commit()
        return cursor.rowcount

    def execute(self, sql: str, params: List[Any] = None) -> List[Dict[str, Any]]:
        """Execute raw SQL."""
        conn = self.connect()
        cursor = conn.cursor()

        logger.debug(f"Raw SQL: {sql}")
        cursor.execute(sql, params or [])

        if sql.strip().upper().startswith("SELECT"):
            return [dict(row) for row in cursor.fetchall()]

        conn.commit()
        return []

    def execute_script(self, sql_script: str) -> None:
        """Execute a SQL script (e.g., CREATE TABLE statements)."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


# -- Convenience functions --

def get_service(db_path: str = None) -> SQLiteService:
    """Get a SQLiteService instance."""
    return SQLiteService(db_path)


# Backward compatibility
SQLiteQueryService = SQLiteService
''',
    },
    "database.py": {
        "target": PROJECT_ROOT / "database/core/storage/sqlite/database.py",
        "content": '''# database/core/storage/sqlite/database.py

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
''',
    },
    "base_repository.py": {
        "target": PROJECT_ROOT / "database/core/repositories/base_repository.py",
        "content": '''from database.core.storage.sqlite.sqlite_service import SQLiteService


class BaseRepository:
    """
    Base repository backed by SQLite cache.
    Uses SQLiteService for all operations.
    """

    TABLE = None

    def __init__(self):
        self.service = SQLiteService()

    def search(self, domain=None, fields=None, limit=None, order=None):
        """Search records matching domain."""
        return self.service.search(
            table=self.TABLE,
            domain=domain,
            fields=fields,
            limit=limit,
            order=order,
        )

    def read(self, ids, fields=None):
        """Read records by ID(s)."""
        return self.service.read(
            table=self.TABLE,
            ids=ids,
            fields=fields,
        )

    def count(self, domain=None):
        """Count records matching domain."""
        return self.service.count(
            table=self.TABLE,
            conditions=domain,
        )
''',
    },
}


def backup_file(path: Path):
    backup = path.with_suffix(path.suffix + ".bak")
    if path.exists():
        shutil.copy2(path, backup)
        print(f"  Backed up: {path.name} -> {backup.name}")
    return backup


def install():
    print("=" * 60)
    print("  Odoo AI Audit Platform -- DB Interface Unification")
    print("=" * 60)
    print()

    # Backup
    print("[1/4] Backing up old files...")
    for name, info in FILES.items():
        backup_file(info["target"])
    print()

    # Install
    print("[2/4] Installing new files...")
    for name, info in FILES.items():
        info["target"].write_text(info["content"], encoding="utf-8")
        print(f"  Installed: {name}")
    print()

    # Verify imports
    print("[3/4] Verifying imports...")
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from database.core.storage.sqlite.sqlite_service import SQLiteService
        from database.core.storage.sqlite.database import SQLiteDatabase
        from database.core.repositories.base_repository import BaseRepository
        print("  All imports successful!")
    except Exception as e:
        print(f"  Import error: {e}")
        return False
    print()

    # Run tests
    print("[4/4] Running tests...")
    import subprocess
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/unit/", "-v", "--tb=short"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        print("\n  Tests FAILED!")
        return False

    print()
    print("=" * 60)
    print("  Installation complete!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = install()
    sys.exit(0 if success else 1)
