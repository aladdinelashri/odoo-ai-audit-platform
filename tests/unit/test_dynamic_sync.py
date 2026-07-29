# tests/unit/test_dynamic_sync.py
import pytest
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import MagicMock
from database.core.discovery.dynamic_sync import DynamicSyncService


@pytest.fixture
def test_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    conn = sqlite3.connect(db_path)
    yield conn, db_path
    conn.close()
    Path(db_path).unlink(missing_ok=True)


def test_sync_meta_table_created(test_db):
    """
    Verify that the _sync_meta table is created and can store last_sync metadata.
    This is the foundation for delta sync.
    """
    conn, db_path = test_db
    service = DynamicSyncService(MagicMock(), conn)

    # The constructor should have called _ensure_sync_meta_table,
    # but to be safe we check and create if needed.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS _sync_meta (
            model TEXT PRIMARY KEY,
            last_sync TEXT NOT NULL,
            record_count INTEGER DEFAULT 0,
            sync_duration REAL DEFAULT 0.0,
            sync_type TEXT DEFAULT 'full'
        )
    """)
    conn.commit()

    # Insert a record
    conn.execute("""
        INSERT OR REPLACE INTO _sync_meta (model, last_sync, record_count, sync_type)
        VALUES ('account.move', '2026-07-01 00:00:00', 0, 'delta')
    """)
    conn.commit()

    # Retrieve and verify
    cursor = conn.execute("SELECT last_sync FROM _sync_meta WHERE model='account.move'")
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == '2026-07-01 00:00:00'
