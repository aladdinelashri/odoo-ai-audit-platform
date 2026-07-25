"""
Tests for SQLiteService -- covers all operators, field mapping, and edge cases.
"""
import pytest
import sqlite3
import tempfile
import os
from database.core.storage.sqlite.sqlite_service import SQLiteService


@pytest.fixture
def db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, label TEXT, val REAL, num INTEGER)")
    conn.executemany("INSERT INTO test (label, val, num) VALUES (?, ?, ?)", [
        ("Alice", 100.0, 1),
        ("Bob", 200.0, 2),
        ("Charlie", 50.0, 3),
        ("Diana", 300.0, 4),
    ])
    conn.commit()
    conn.close()
    service = SQLiteService(db_path=path)
    yield service
    service.close()
    os.unlink(path)


@pytest.fixture
def pos_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE pos_orders (
            id INTEGER PRIMARY KEY,
            order_name TEXT,
            order_date TEXT,
            amount_total REAL,
            state TEXT,
            session_id INTEGER,
            company_id INTEGER,
            partner_id INTEGER
        )
    """)
    conn.executemany("""
        INSERT INTO pos_orders (order_name, order_date, amount_total, state, session_id, company_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ("ORD-001", "2026-07-01", 150.0, "done", 1, 1),
        ("ORD-002", "2026-07-02", 250.0, "done", 1, 1),
        ("ORD-003", "2026-07-03", -50.0, "done", 2, 1),
        ("ORD-004", "2026-07-04", 0.0, "draft", 2, 2),
        ("ORD-005", "2026-07-05", 500.0, "done", 3, 2),
    ])
    conn.commit()
    conn.close()
    service = SQLiteService(db_path=path)
    yield service
    service.close()
    os.unlink(path)


def test_query_equal(db):
    rows = db.query("test", conditions=[("label", "=", "Alice")])
    assert len(rows) == 1
    assert rows[0]["label"] == "Alice"


def test_query_not_equal(db):
    rows = db.query("test", conditions=[("label", "!=", "Alice")])
    assert len(rows) == 3


def test_query_greater_than(db):
    rows = db.query("test", conditions=[("val", ">", 75)])
    assert len(rows) == 3


def test_query_less_than(db):
    rows = db.query("test", conditions=[("val", "<", 100)])
    assert len(rows) == 1
    assert rows[0]["label"] == "Charlie"


def test_query_greater_equal(db):
    rows = db.query("test", conditions=[("val", ">=", 100)])
    assert len(rows) == 3


def test_query_less_equal(db):
    rows = db.query("test", conditions=[("val", "<=", 100)])
    assert len(rows) == 2


def test_query_like(db):
    rows = db.query("test", conditions=[("label", "like", "Ali")])
    assert len(rows) == 1
    assert rows[0]["label"] == "Alice"


def test_query_like_partial(db):
    rows = db.query("test", conditions=[("label", "like", "li")])
    assert len(rows) == 2


def test_query_in(db):
    rows = db.query("test", conditions=[("label", "in", ["Alice", "Bob"])])
    assert len(rows) == 2


def test_query_between(db):
    rows = db.query("test", conditions=[("val", "between", [50, 150])])
    assert len(rows) == 2


def test_query_multiple_conditions(db):
    rows = db.query("test", conditions=[
        ("val", ">", 75),
        ("num", ">=", 2),
    ])
    assert len(rows) == 2  # Bob (200, num=2), Diana (300, num=4)


def test_query_limit(db):
    rows = db.query("test", limit=2)
    assert len(rows) == 2


def test_query_order_by(db):
    rows = db.query("test", order_by="val")
    vals = [r["val"] for r in rows]
    assert vals == [50.0, 100.0, 200.0, 300.0]


def test_query_offset(db):
    rows = db.query("test", order_by="val", limit=2, offset=1)
    assert len(rows) == 2
    assert rows[0]["val"] == 100.0


def test_query_columns(db):
    rows = db.query("test", columns=["label", "val"])
    assert set(rows[0].keys()) == {"label", "val"}


def test_count_all(db):
    assert db.count("test") == 4


def test_count_with_conditions(db):
    assert db.count("test", [("val", ">=", 100)]) == 3


def test_sum(db):
    assert db.sum("test", "val") == 650.0


def test_sum_with_conditions(db):
    assert db.sum("test", "val", [("num", ">", 2)]) == 350.0  # Charlie 50 + Diana 300


def test_insert(db):
    new_id = db.insert("test", {"label": "Eve", "val": 400.0, "num": 5})
    assert new_id == 5
    rows = db.query("test", conditions=[("label", "=", "Eve")])
    assert len(rows) == 1
    assert rows[0]["val"] == 400.0


def test_insert_many(db):
    count = db.insert_many("test", [
        {"label": "Frank", "val": 10.0, "num": 1},
        {"label": "Grace", "val": 20.0, "num": 2},
    ])
    assert count == 2
    assert db.count("test") == 6


def test_execute_raw_select(db):
    rows = db.execute("SELECT * FROM test WHERE val > ?", [100])
    assert len(rows) == 2


def test_execute_raw_insert(db):
    db.execute("INSERT INTO test (label, val, num) VALUES (?, ?, ?)", ["Hank", 99.0, 1])
    assert db.count("test") == 5


# POS-specific tests with FIELD_MAP

def test_field_mapping_name_to_order_name(pos_db):
    rows = pos_db.query("pos_orders", conditions=[("name", "=", "ORD-001")])
    assert len(rows) == 1
    assert rows[0]["order_name"] == "ORD-001"


def test_field_mapping_amount_total(pos_db):
    rows = pos_db.query("pos_orders", conditions=[("amount_total", ">", 200)])
    assert len(rows) == 2


def test_field_mapping_date_order(pos_db):
    rows = pos_db.query("pos_orders", conditions=[("date_order", ">=", "2026-07-04")])
    assert len(rows) == 2


def test_field_mapping_state(pos_db):
    rows = pos_db.query("pos_orders", conditions=[("state", "=", "done")])
    assert len(rows) == 4  # ORD-001, 002, 003, 005


def test_field_mapping_combined(pos_db):
    rows = pos_db.query("pos_orders", conditions=[
        ("state", "=", "done"),
        ("amount_total", ">", 100),
    ])
    assert len(rows) == 3  # ORD-001 (150), ORD-002 (250), ORD-005 (500)


def test_pos_count(pos_db):
    assert pos_db.count("pos_orders") == 5
    assert pos_db.count("pos_orders", [("state", "=", "done")]) == 4


def test_pos_sum_amount_total(pos_db):
    total = pos_db.sum("pos_orders", "amount_total")
    assert total == 850.0


def test_pos_sum_with_refunds(pos_db):
    total = pos_db.sum("pos_orders", "amount_total", [("amount_total", ">", 0)])
    assert total == 900.0
