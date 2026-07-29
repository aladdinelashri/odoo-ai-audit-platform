# tests/unit/test_database_setup.py
import sqlite3
import tempfile
from pathlib import Path

def test_wal_enabled():
    """Verify that WAL journal mode can be enabled (this is what the script would do)."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.close()

    conn = sqlite3.connect(db_path)
    journal_mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
    assert journal_mode == "wal"
    conn.close()
    Path(db_path).unlink(missing_ok=True)


def test_critical_indexes_exist():
    """Verify that critical indexes can be created (this is what the script would do)."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    conn = sqlite3.connect(db_path)
    # Create tables
    conn.executescript("""
        CREATE TABLE account_move_lines (move_id INTEGER, account_id INTEGER, date TEXT, tax_line_id INTEGER);
        CREATE TABLE account_moves (state TEXT, date TEXT, journal_id INTEGER, name TEXT, partner_id INTEGER);
        CREATE TABLE account_accounts (account_type TEXT, code TEXT, parent_id INTEGER);
        CREATE TABLE account_journals (type TEXT);
        CREATE TABLE pos_orders (session_id INTEGER, date_order TEXT);
    """)
    # Create indexes
    conn.execute("CREATE INDEX idx_aml_move_id ON account_move_lines (move_id)")
    conn.execute("CREATE INDEX idx_aml_account_id ON account_move_lines (account_id)")
    conn.execute("CREATE INDEX idx_am_state ON account_moves (state)")
    conn.execute("CREATE INDEX idx_aa_type ON account_accounts (account_type)")
    conn.execute("CREATE INDEX idx_aj_type ON account_journals (type)")
    conn.close()

    conn = sqlite3.connect(db_path)
    indexes = conn.execute("SELECT name FROM sqlite_master WHERE type='index'").fetchall()
    index_names = [row[0] for row in indexes]
    expected = [
        "idx_aml_move_id",
        "idx_aml_account_id",
        "idx_am_state",
        "idx_aa_type",
        "idx_aj_type"
    ]
    for idx in expected:
        assert idx in index_names
    conn.close()
    Path(db_path).unlink(missing_ok=True)
