# database/core/storage/postgresql/postgresql_pool.py

import re
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

from ..base_pool import DatabasePool


# Detect write operations that must be committed
_WRITE_OPS = re.compile(
    r'^\s*(INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|TRUNCATE|MERGE|UPSERT)\s',
    re.IGNORECASE
)


class PostgreSQLPool(DatabasePool):
    def __init__(self, dsn: str, min_conn: int = 1, max_conn: int = 20):
        self._dsn = dsn
        self._pool = ThreadedConnectionPool(
            minconn=min_conn,
            maxconn=max_conn,
            dsn=dsn,
            cursor_factory=RealDictCursor,
        )

    @staticmethod
    def _is_write_query(query: str) -> bool:
        return bool(_WRITE_OPS.match(query))

    def get_connection(self):
        conn = self._pool.getconn()
        try:
            yield conn
        finally:
            self._pool.putconn(conn)

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> None:
        conn = self._pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self._pool.putconn(conn)

    def execute_many(self, query: str, params_list: List[Tuple]) -> None:
        conn = self._pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.executemany(query, params_list)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self._pool.putconn(conn)

    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        conn = self._pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                row = cur.fetchone()

            # ROOT CAUSE FIX: auto-commit write operations even in fetch_one
            if self._is_write_query(query):
                conn.commit()

            return dict(row) if row else None

        except psycopg2.ProgrammingError as e:
            # fetchone() on no-result queries (e.g. CREATE) raises ProgrammingError
            if self._is_write_query(query):
                conn.commit()
                return None
            raise
        except Exception:
            conn.rollback()
            raise
        finally:
            self._pool.putconn(conn)

    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        conn = self._pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                rows = cur.fetchall()
            return [dict(r) for r in rows] if rows else []
        except Exception:
            conn.rollback()
            raise
        finally:
            self._pool.putconn(conn)

    def close(self) -> None:
        if self._pool:
            self._pool.closeall()
