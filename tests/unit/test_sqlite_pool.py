# tests/unit/test_sqlite_pool.py
import pytest
import tempfile
import sqlite3
from pathlib import Path
from database.core.storage.sqlite.sqlite_pool import SQLitePool


def test_pragmas_set():
    """Verify that SQLitePool sets the expected pragmas."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    SQLitePool._instance = None
    SQLitePool.initialize(db_path)
    conn = SQLitePool.get_connection()

    wal = conn.execute("PRAGMA journal_mode").fetchone()[0]
    assert wal == "wal"

    cache = conn.execute("PRAGMA cache_size").fetchone()[0]
    assert cache == -64000

    mmap = conn.execute("PRAGMA mmap_size").fetchone()[0]
    assert mmap == 268435456

    conn.close()
    SQLitePool._instance = None
    Path(db_path).unlink(missing_ok=True)
