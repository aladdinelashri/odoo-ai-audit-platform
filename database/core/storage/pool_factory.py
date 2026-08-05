"""Factory for creating database pools."""
from .base_pool import DatabasePool
from .sqlite.sqlite_pool import SQLitePool
from .postgresql.postgresql_pool import PostgreSQLPool
import os

# Singleton caches
_pg_pool = None
_sqlite_pool = None


def create_pool() -> DatabasePool:
    """Create a database pool based on DATABASE_TYPE env var."""
    db_type = os.getenv("DATABASE_TYPE", "sqlite").lower()
    if db_type == "postgresql":
        dsn = os.getenv("POSTGRES_DSN")
        if not dsn:
            raise ValueError("POSTGRES_DSN environment variable required for PostgreSQL")
        return PostgreSQLPool(dsn, min_conn=1, max_conn=20)
    else:
        db_path = os.getenv("AUDIT_DB_PATH", "database/storage/audit.db")
        return SQLitePool(db_path)


def get_db_pool() -> DatabasePool:
    """Get the PostgreSQL pool (main database for reports, users, audit logs).
    
    FastAPI dependency. Cached singleton.
    """
    global _pg_pool
    if _pg_pool is None:
        dsn = os.getenv("POSTGRES_DSN")
        if not dsn:
            raise ValueError("POSTGRES_DSN environment variable required for PostgreSQL")
        _pg_pool = PostgreSQLPool(dsn, min_conn=1, max_conn=20)
    return _pg_pool


def get_sqlite_pool() -> DatabasePool:
    """Get the SQLite pool (Odoo cache, pos_orders table).
    
    FastAPI dependency. Cached singleton.
    """
    global _sqlite_pool
    if _sqlite_pool is None:
        db_path = os.getenv("AUDIT_DB_PATH", "database/storage/audit.db")
        _sqlite_pool = SQLitePool(db_path)
    return _sqlite_pool
