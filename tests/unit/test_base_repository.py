"""Tests for BaseRepository — fixed to work with SQLiteService."""

import pytest
import sqlite3
import tempfile
import os
from database.core.repositories.base_repository import BaseRepository


class TestRepository(BaseRepository):
    """Concrete repo for testing."""
    TABLE = "test_items"


@pytest.fixture
def repo():
    """Create a temporary repo with test data."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE test_items (id INTEGER PRIMARY KEY, name TEXT, price REAL, active INTEGER)")
    conn.executemany(
        "INSERT INTO test_items (name, price, active) VALUES (?, ?, ?)",
        [
            ("Apple", 1.50, 1),
            ("Banana", 0.75, 1),
            ("Cherry", 2.00, 0),
            ("Date", 3.00, 1),
        ],
    )
    conn.commit()
    conn.close()

    repo = TestRepository()
    repo.service.db_path = path
    repo.service.conn = None  # Force reconnect

    yield repo

    repo.service.close()
    os.unlink(path)


# ─── search ───
def test_search_all(repo):
    rows = repo.search()
    assert len(rows) == 4


def test_search_with_domain(repo):
    rows = repo.search(domain=[("active", "=", 1)])
    assert len(rows) == 3


def test_search_with_fields(repo):
    rows = repo.search(fields=["name", "price"])
    assert set(rows[0].keys()) == {"name", "price"}


def test_search_with_limit(repo):
    rows = repo.search(limit=2)
    assert len(rows) == 2


def test_search_with_order(repo):
    rows = repo.search(order="price DESC")
    assert rows[0]["name"] == "Date"
    assert rows[0]["price"] == 3.00


def test_search_with_multiple_conditions(repo):
    rows = repo.search(domain=[("active", "=", 1), ("price", ">", 1.00)])
    assert len(rows) == 2
    names = {r["name"] for r in rows}
    assert names == {"Apple", "Date"}


# ─── read ───
def test_read_single_id(repo):
    rows = repo.read(1)
    assert len(rows) == 1
    assert rows[0]["name"] == "Apple"


def test_read_multiple_ids(repo):
    rows = repo.read([1, 2])
    assert len(rows) == 2
    names = {r["name"] for r in rows}
    assert names == {"Apple", "Banana"}


def test_read_with_fields(repo):
    rows = repo.read(1, fields=["name"])
    assert set(rows[0].keys()) == {"name"}


def test_read_empty_ids(repo):
    rows = repo.read([])
    assert rows == []


# ─── count ───
def test_count_all(repo):
    assert repo.count() == 4


def test_count_with_domain(repo):
    assert repo.count(domain=[("active", "=", 0)]) == 1


def test_count_no_match(repo):
    assert repo.count(domain=[("price", ">", 100)]) == 0
