import sqlite3
import logging
import threading
import os
from contextlib import contextmanager
from typing import Optional, Tuple, List, Dict, Any

logger = logging.getLogger(__name__)


class SQLitePool:
    """Thread-safe SQLite connection pool (singleton)."""

    _instance: Optional["SQLitePool"] = None
    _lock = threading.Lock()

    def __new__(cls, db_path: str = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._initialized = False
                    cls._instance = instance
        return cls._instance

    def __init__(self, db_path: str = None):
        if getattr(self, "_initialized", False):
            return
        self.db_path = db_path or os.getenv("SQLITE_PATH", "database/storage/audit.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._connections: Dict[int, sqlite3.Connection] = {}
        self._local = threading.local()
        self._initialized = True
        # Enable WAL mode on initialization
        with self.connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA foreign_keys=ON")
        logger.info("sqlite_pool.initialized", path=self.db_path)

    @contextmanager
    def connection(self):
        """Context manager for SQLite connection."""
        thread_id = threading.get_ident()

        if hasattr(self._local, "connection") and self._local.connection:
            conn = self._local.connection
        else:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            self._local.connection = conn
            self._connections[thread_id] = conn

        try:
            yield conn
        except Exception:
            conn.rollback()
            raise

    # Alias for compatibility with reports.py
    get_connection = connection

    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        """Execute query and return first row as dict, or None."""
        with self.connection() as conn:
            cursor = conn.execute(query, params or ())
            row = cursor.fetchone()
            if row is None:
                return None
            return dict(row)

    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """Execute query and return all rows as list of dicts."""
        with self.connection() as conn:
            cursor = conn.execute(query, params or ())
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> None:
        """Execute a query that does not return rows (INSERT, UPDATE, DELETE, etc.)."""
        with self.connection() as conn:
            conn.execute(query, params or ())
            conn.commit()

    def execute_many(self, query: str, params_list: List[Tuple]) -> None:
        """Execute a parametrized query for multiple parameter sets."""
        with self.connection() as conn:
            conn.executemany(query, params_list)
            conn.commit()

    def close(self) -> None:
        """Close all connections held by the pool."""
        for thread_id, conn in list(self._connections.items()):
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    logger.warning(f"Error closing connection for thread {thread_id}: {e}")
        self._connections.clear()
        logger.info("All SQLite connections closed")

    # --- Legacy classmethods for backward compatibility ---

    @classmethod
    def get_connection(cls):
        """Class-level context manager delegating to singleton instance."""
        instance = cls._instance
        if instance is None:
            instance = cls()
        return instance.connection()

    @classmethod
    def execute(cls, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """Execute query and return all rows as sqlite3.Row objects."""
        with cls.connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    @classmethod
    def execute_one(cls, query: str, params: Tuple = ()) -> Optional[sqlite3.Row]:
        """Execute query and return first row as sqlite3.Row, or None."""
        with cls.connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchone()

    @classmethod
    def close_all(cls) -> None:
        """Close all connections (same as close instance method)."""
        instance = cls._instance
        if instance:
            instance.close()


# Module-level singleton accessor
_sqlite_pool = None


def get_sqlite_pool() -> SQLitePool:
    """Get or create the global SQLitePool instance."""
    global _sqlite_pool
    if _sqlite_pool is None:
        _sqlite_pool = SQLitePool()
    return _sqlite_pool
