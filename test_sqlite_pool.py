import pytest
from database.core.storage.sqlite.sqlite_pool import SQLitePool

def test_pool_singleton():
    SQLitePool.initialize(":memory:")
    pool1 = SQLitePool._instance
    SQLitePool.initialize(":memory:")  # should reuse
    pool2 = SQLitePool._instance
    assert pool1 is pool2
    SQLitePool._instance = None  # clean up after this test

def test_connection_reuse():
    SQLitePool.initialize(":memory:")
    conn1 = SQLitePool.get_connection()
    conn2 = SQLitePool.get_connection()
    assert conn1 is conn2
    SQLitePool._instance = None  # clean up

def test_pragmas_set(tmp_path):
    # IMPORTANT: Reset the singleton so that it will create a new file-based connection
    SQLitePool._instance = None
    db_path = str(tmp_path / "test.db")
    SQLitePool.initialize(db_path)
    conn = SQLitePool.get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode")
    mode = cursor.fetchone()[0]
    assert mode.lower() == "wal", f"Expected wal, got {mode}"
    cursor.execute("PRAGMA cache_size")
    assert cursor.fetchone()[0] == -64000  # 64 MB
    SQLitePool._instance = None  # clean up
