# tests/unit/test_audit_result.py
import pytest
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch
from database.core.storage.sqlite.sqlite_pool import SQLitePool
from database.core.audits.accounting.journal_audit import JournalAudit


@pytest.fixture(scope="function")
def audit_db():
    """Create a temporary SQLite database with schema."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE account_moves (
            id INTEGER PRIMARY KEY,
            name TEXT,
            journal_id INTEGER,
            partner_id INTEGER,
            amount_total REAL,
            state TEXT,
            date TEXT,
            move_type TEXT,
            create_date TEXT,
            write_date TEXT
        );
        CREATE TABLE account_move_lines (
            id INTEGER PRIMARY KEY,
            move_id INTEGER,
            account_id INTEGER,
            debit REAL,
            credit REAL,
            balance REAL,
            name TEXT,
            date TEXT,
            tax_line_id INTEGER,
            tax_base_amount REAL
        );
        CREATE TABLE account_accounts (
            id INTEGER PRIMARY KEY,
            code TEXT,
            name TEXT,
            account_type TEXT,
            parent_id INTEGER
        );
        CREATE TABLE account_journals (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT
        );
        CREATE TABLE account_tax (
            id INTEGER PRIMARY KEY,
            name TEXT,
            amount REAL
        );
        CREATE TABLE res_partner (
            id INTEGER PRIMARY KEY,
            name TEXT
        );
    """)
    conn.commit()

    with patch.object(SQLitePool, 'get_connection', return_value=conn):
        yield conn

    conn.close()
    Path(db_path).unlink(missing_ok=True)
    SQLitePool._instance = None


def test_audit_result_contains_expected_fields(audit_db):
    """Verify that the result dict from an audit has the required fields."""
    conn = audit_db
    # Insert a balanced move so the audit passes
    conn.executescript("""
        INSERT INTO account_moves (id, name, journal_id, partner_id, amount_total, state, date, move_type)
        VALUES (1, 'INV/001', 1, 100, 100.0, 'posted', '2026-07-01', 'entry');
        INSERT INTO account_move_lines (move_id, account_id, debit, credit, balance)
        VALUES (1, 1, 100, 0, 100), (1, 2, 0, 100, -100);
    """)
    conn.commit()

    audit = JournalAudit()
    result = audit.analyze()

    # Assert that all expected keys are present
    expected_keys = {"audit_code", "status", "findings", "performance"}
    assert expected_keys.issubset(result.keys())

    # Assert that status is a string and findings is a list
    assert isinstance(result["status"], str)
    assert isinstance(result["findings"], list)
    assert isinstance(result["performance"], dict)

    # Check that performance contains at least one of the expected timing keys
    # The audit currently returns 'query_time_ms' and 'queries_executed'
    # Accept either 'total_time_ms' or 'query_time_ms'
    perf_keys = result["performance"].keys()
    assert any(k in perf_keys for k in ["total_time_ms", "query_time_ms", "execution_time_ms"])
    assert "queries_executed" in perf_keys
