"""
SQLite Connection Pool with WAL Mode and Performance Optimizations.
"""

import sqlite3
import threading
from contextlib import contextmanager
from typing import Optional, Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)


class SQLitePool:
    """Thread-safe SQLite connection pool with performance optimizations."""
    
    _instance = None
    _lock = threading.Lock()
    _connections: Dict[int, sqlite3.Connection] = {}
    _db_path: str = "database/storage/audit.db"
    _initialized: bool = False
    
    def __new__(cls, db_path: str = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    if db_path:
                        cls._db_path = db_path
        return cls._instance
    
    @classmethod
    def initialize(cls, db_path: str) -> None:
        cls._db_path = db_path
        cls._initialized = True
        logger.info(f"SQLitePool initialized: {db_path}")
    
    @classmethod
    def _get_thread_id(cls) -> int:
        return threading.current_thread().ident
    
    @classmethod
    def _configure_connection(cls, conn: sqlite3.Connection) -> None:
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        conn.execute("PRAGMA cache_size = -64000")
        conn.execute("PRAGMA temp_store = MEMORY")
        conn.execute("PRAGMA mmap_size = 268435456")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA optimize")
        conn.row_factory = sqlite3.Row
    
    @classmethod
    def get_connection(cls, db_path: str = None) -> sqlite3.Connection:
        if db_path is None:
            db_path = cls._db_path
        thread_id = cls._get_thread_id()
        if thread_id not in cls._connections or cls._connections[thread_id] is None:
            conn = sqlite3.connect(db_path, check_same_thread=False)
            cls._configure_connection(conn)
            cls._connections[thread_id] = conn
        return cls._connections[thread_id]
    
    @classmethod
    @contextmanager
    def connection(cls, db_path: str = None):
        conn = cls.get_connection(db_path)
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise
        else:
            conn.commit()
    
    @classmethod
    def execute(cls, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        with cls.connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()
    
    @classmethod
    def execute_one(cls, query: str, params: Tuple = ()) -> Optional[sqlite3.Row]:
        with cls.connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchone()
    
    @classmethod
    def close_all(cls) -> None:
        for thread_id, conn in cls._connections.items():
            if conn:
                conn.close()
        cls._connections.clear()
