"""Tests for AuditContextBuilder and related dataclasses."""

import pytest
from unittest.mock import MagicMock
from datetime import datetime
from database.core.context.context_builder import (
    AuditContextBuilder,
    AuditContext,
    BusinessUnit,
    SessionContext,
)


# ─── BusinessUnit ───
def test_business_unit_from_row():
    row = {"id": 5, "name": "Downtown Branch", "company_id": 1, "code": "DT001"}
    bu = BusinessUnit.from_row(row)
    assert bu.id == 5
    assert bu.name == "Downtown Branch"
    assert bu.company_id == 1
    assert bu.code == "DT001"


def test_business_unit_from_row_defaults():
    row = {"id": 1}
    bu = BusinessUnit.from_row(row)
    assert bu.name == "Unknown"
    assert bu.company_id is None
    assert bu.code is None


# ─── SessionContext ───
def test_session_context_creation():
    session = SessionContext(
        id=10,
        name="Morning Shift",
        start_at=datetime(2026, 7, 25, 8, 0),
        state="opened",
        config_id=2,
        business_unit_id=5,
    )
    assert session.id == 10
    assert session.name == "Morning Shift"
    assert session.state == "opened"


# ─── AuditContext ───
def test_audit_context_to_dict():
    bu = BusinessUnit(id=1, name="Main")
    ctx = AuditContext(
        business_unit=bu,
        date_from="2026-07-01",
        date_to="2026-07-25",
        filters={"branch_id": 3},
    )
    d = ctx.to_dict()
    assert d["business_unit"]["id"] == 1
    assert d["business_unit"]["name"] == "Main"
    assert d["date_from"] == "2026-07-01"
    assert d["filters"]["branch_id"] == 3


def test_audit_context_empty():
    ctx = AuditContext()
    d = ctx.to_dict()
    assert d["business_unit"] is None
    assert d["session"] is None
    assert d["filters"] == {}


# ─── AuditContextBuilder: with business_unit_id ───
def test_build_with_business_unit_id():
    mock_sqlite = MagicMock()
    mock_sqlite.query.return_value = [
        {"id": 1, "name": "Main Branch", "company_id": 1}
    ]

    builder = AuditContextBuilder(sqlite_service=mock_sqlite)
    ctx = builder.build(business_unit_id=1)

    assert ctx.business_unit is not None
    assert ctx.business_unit.id == 1
    assert ctx.business_unit.name == "Main Branch"
    mock_sqlite.query.assert_called_once()


# ─── AuditContextBuilder: with session_id ───
def test_build_with_session_id():
    mock_sqlite = MagicMock()
    mock_sqlite.query.side_effect = [
        # Session query
        [{"id": 5, "name": "Session 5", "business_unit_id": 2, "state": "closed"}],
        # Business unit query
        [{"id": 2, "name": "Branch B", "company_id": 1}],
    ]

    builder = AuditContextBuilder(sqlite_service=mock_sqlite)
    ctx = builder.build(session_id=5)

    assert ctx.session is not None
    assert ctx.session.id == 5
    assert ctx.session.name == "Session 5"
    assert ctx.business_unit is not None
    assert ctx.business_unit.id == 2


# ─── AuditContextBuilder: date range ───
def test_build_with_date_range():
    mock_sqlite = MagicMock()
    builder = AuditContextBuilder(sqlite_service=mock_sqlite)
    ctx = builder.build(date_from="2026-01-01", date_to="2026-12-31")

    assert ctx.date_from == "2026-01-01"
    assert ctx.date_to == "2026-12-31"
    assert ctx.business_unit is None


# ─── AuditContextBuilder: fallback session map ───
def test_build_from_session_map():
    mock_sqlite = MagicMock()
    mock_sqlite.query.side_effect = [
        # session_business_units
        [{"session_id": 10, "business_unit_id": 3}],
        # business unit
        [{"id": 3, "name": "Branch C", "company_id": 1}],
        # session
        [{"id": 10, "name": "Session 10", "state": "opened"}],
    ]

    builder = AuditContextBuilder(sqlite_service=mock_sqlite)
    ctx = builder.build_from_session_map(session_id=10)

    assert ctx.business_unit is not None
    assert ctx.business_unit.id == 3
    assert ctx.session is not None
    assert ctx.session.id == 10


# ─── AuditContextBuilder: missing data ───
def test_build_business_unit_not_found():
    mock_sqlite = MagicMock()
    mock_sqlite.query.return_value = []  # No rows found

    builder = AuditContextBuilder(sqlite_service=mock_sqlite)
    ctx = builder.build(business_unit_id=999)

    assert ctx.business_unit is None
