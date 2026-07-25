#!/usr/bin/env python3
"""
Odoo AI Audit Platform — Auto-Install Script
Replaces broken components and installs new tests.
Run on server: python3 install_audit_updates.py
"""

import os
import shutil
from pathlib import Path

# ─── CONFIG ───
PROJECT_ROOT = Path("/home/helioit/odoo-ai-audit-platform")
if not PROJECT_ROOT.exists():
    PROJECT_ROOT = Path.cwd()

FILES = {
    # 1. Fix BaseRepository
    "database/core/repositories/base_repository.py": """"""Base repository backed by SQLite cache."""

from database.core.storage.sqlite.sqlite_service import SQLiteService


class BaseRepository:
    """
    Base repository backed by SQLite cache.
    Translates Odoo-style domain/fields to SQLiteService query format.
    """

    TABLE = None

    def __init__(self):
        self.service = SQLiteService()

    def search(self, domain=None, fields=None, limit=None, order=None):
        """
        Search records matching domain.

        Args:
            domain: List of tuples [(field, operator, value), ...]
            fields: List of column names to select
            limit: Max rows to return
            order: ORDER BY clause string

        Returns:
            List of dictionaries
        """
        return self.service.query(
            table=self.TABLE,
            columns=fields,
            conditions=domain,
            order_by=order,
            limit=limit,
        )

    def read(self, ids, fields=None):
        """
        Read records by IDs.

        Args:
            ids: Single ID or list of IDs
            fields: List of column names to select

        Returns:
            List of dictionaries
        """
        if not ids:
            return []

        id_list = ids if isinstance(ids, (list, tuple)) else [ids]

        return self.service.query(
            table=self.TABLE,
            columns=fields,
            conditions=[("id", "in", id_list)],
        )

    def count(self, domain=None):
        """
        Count records matching domain.

        Args:
            domain: List of tuples [(field, operator, value), ...]

        Returns:
            Integer count
        """
        return self.service.count(
            table=self.TABLE,
            conditions=domain,
        )
""",

    # 2. Fix Audit Registry
    "database/core/audits/registry/audit_registry.py": """"""
Audit Registry — Registry Pattern for all audit modules.
Central registry to dynamically discover and run audits.
"""

import importlib
import logging
from typing import Dict, Callable, Any, Optional
from dataclasses import dataclass

from config.logging import get_logger

logger = get_logger('audit.registry')


@dataclass
class AuditInfo:
    """Metadata for a registered audit."""
    name: str
    code: str
    description: str
    module_path: str
    func_name: str = 'run'
    category: str = 'pos'


class AuditRegistry:
    """
    Central registry for all audit modules.
    Allows dynamic discovery without hard-coding imports.
    """

    def __init__(self):
        self._audits: Dict[str, AuditInfo] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register all built-in audits."""
        defaults = [
            AuditInfo('missing_receipts', 'MISSING_RCPT', 'Detect missing receipts', 'database.core.audits.missing_receipts_audit'),
            AuditInfo('refunds', 'REFUNDS', 'Analyze refund patterns', 'database.core.audits.refunds.refund_spike_audit'),
            AuditInfo('daily_summary', 'DAILY_SUM', 'Daily POS summary', 'database.core.audits.pos_daily_summary_audit'),
            AuditInfo('monthly_summary', 'MONTHLY_SUM', 'Monthly POS summary', 'database.core.audits.pos_monthly_summary_audit'),
            AuditInfo('sales_summary', 'SALES_SUM', 'Sales performance summary', 'database.core.audits.pos_sales_summary_audit'),
            AuditInfo('payment_methods', 'PAY_METH', 'Payment method breakdown', 'database.core.audits.payment_method_summary_audit'),
            AuditInfo('cashier_performance', 'CASH_PERF', 'Cashier performance KPI', 'database.core.audits.cashier_performance_audit'),
            AuditInfo('session', 'SESSION', 'POS session audit', 'database.core.audits.session_audit'),
            AuditInfo('business_unit_kpi', 'BU_KPI', 'Business unit KPI', 'database.core.audits.business_unit_kpi_audit'),
            AuditInfo('category_ranking', 'CAT_RANK', 'Category daily ranking', 'database.core.audits.pos_category_daily_ranking_audit'),
        ]
        for audit in defaults:
            self.register(audit)

    def register(self, audit: AuditInfo) -> None:
        """Register an audit module."""
        self._audits[audit.name] = audit
        logger.debug(f"Registered audit: {audit.name} ({audit.code})")

    def get(self, name: str) -> Optional[AuditInfo]:
        """Get audit metadata by name."""
        return self._audits.get(name)

    def list_audits(self, category: str = None) -> Dict[str, AuditInfo]:
        """List all registered audits, optionally filtered by category."""
        if category:
            return {k: v for k, v in self._audits.items() if v.category == category}
        return self._audits.copy()

    def run(self, name: str, context, **kwargs) -> Any:
        """
        Dynamically load and run an audit by name.

        Args:
            name: Audit name (e.g., 'missing_receipts')
            context: AuditContext from context_builder
            **kwargs: Additional arguments passed to audit

        Returns:
            Audit result
        """
        audit = self.get(name)
        if not audit:
            raise ValueError(f"Audit '{name}' not found. Available: {list(self._audits.keys())}")

        try:
            module = importlib.import_module(audit.module_path)
            func = getattr(module, audit.func_name, None)

            if not func:
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if callable(attr) and not attr_name.startswith('_'):
                        func = attr
                        break

            if not func:
                raise AttributeError(f"No callable found in {audit.module_path}")

            logger.info(f"Running audit: {audit.name} ({audit.code})")
            return func(context, **kwargs)

        except Exception as e:
            logger.error(f"Failed to run audit '{name}': {e}")
            raise


# Singleton instance
registry = AuditRegistry()
""",

    # 3. Update refunds __init__.py
    "database/core/audits/refunds/__init__.py": """"""Refund audit modules."""

from database.core.audits.refunds.refund_audit import RefundAudit
from database.core.audits.refunds.refund_spike_audit import RefundSpikeAudit

__all__ = ["RefundAudit", "RefundSpikeAudit"]
""",

    # 4. Create RefundSpikeAudit
    "database/core/audits/refunds/refund_spike_audit.py": """"""Refund Spike Detection — flags abnormal refund patterns."""

from database.core.audits.base.base_pos_audit import BasePOSAudit
from database.core.storage.sqlite.database import SQLiteDatabase
from datetime import datetime, timedelta
from collections import Counter


class RefundSpikeAudit(BasePOSAudit):
    """
    Detects refund spikes compared to 30-day moving average.

    Flags HIGH risk if refunds spike > 280% of daily average.
    Flags MEDIUM risk if refunds spike > 150% of daily average.
    """

    code = "refund_spike"
    name = "Refund Spike Detection"

    def __init__(self):
        super().__init__()
        self._db = SQLiteDatabase()

    def analyze(self):
        """
        Analyze refund patterns and detect anomalies.

        Returns:
            dict: Refund statistics, spike ratios, and risk assessment.
        """
        today = datetime.now().strftime("%Y-%m-%d")

        # ─── Today's refunds ───
        today_orders = self.get_orders(
            domain=[
                ("state", "=", "done"),
                ("date_order", "like", f"{today}%"),
            ],
            fields=["id", "amount_total", "date_order", "user_id", "name"],
        )
        today_refunds = [o for o in today_orders if o.get("amount_total", 0) < 0]
        today_count = len(today_refunds)
        today_amount = abs(
            sum(o["amount_total"] for o in today_refunds)
        ) if today_refunds else 0.0

        # ─── 30-day moving average ───
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        rows = self._db.query(
            """
            SELECT 
                COUNT(*) as count,
                COALESCE(SUM(ABS(amount_total)), 0) as amount
            FROM pos_orders
            WHERE amount_total < 0 AND date_order >= ?
            """,
            (thirty_days_ago,),
        )

        hist_count = rows[0]["count"] if rows else 0
        hist_amount = rows[0]["amount"] if rows else 0

        daily_avg = hist_count / 30.0 if hist_count > 0 else 0.0
        daily_avg_amount = hist_amount / 30.0 if hist_amount > 0 else 0.0

        # ─── Spike ratios ───
        spike_ratio = (today_count / daily_avg) if daily_avg > 0 else 0.0
        amount_spike = (today_amount / daily_avg_amount) if daily_avg_amount > 0 else 0.0

        # ─── Risk assessment ───
        risk = "LOW"
        if spike_ratio > 2.8 or amount_spike > 2.8:
            risk = "HIGH"
        elif spike_ratio > 1.5 or amount_spike > 1.5:
            risk = "MEDIUM"

        # ─── Top cashiers by refund count ───
        cashiers = Counter(o.get("user_id", "Unknown") for o in today_refunds)
        top_cashiers = [
            {"cashier_id": c, "refund_count": n}
            for c, n in cashiers.most_common(5)
        ]

        # ─── Top refunds by amount ───
        top_refunds = sorted(
            today_refunds,
            key=lambda o: abs(o.get("amount_total", 0)),
            reverse=True,
        )[:5]
        top_refunds_summary = [
            {
                "order_id": o["id"],
                "order_name": o.get("name", ""),
                "amount": round(abs(o["amount_total"]), 2),
                "cashier_id": o.get("user_id"),
            }
            for o in top_refunds
        ]

        return {
            "today_refunds": today_count,
            "today_amount": round(today_amount, 2),
            "daily_avg_refunds": round(daily_avg, 2),
            "daily_avg_amount": round(daily_avg_amount, 2),
            "spike_ratio": round(spike_ratio, 2),
            "amount_spike": round(amount_spike, 2),
            "risk_level": risk,
            "top_cashiers": top_cashiers,
            "top_refunds": top_refunds_summary,
        }
""",

    # 5. Test: SQLiteService
    "tests/unit/test_sqlite_service.py": """"""Tests for SQLiteService — full operator coverage."""

import pytest
import sqlite3
import tempfile
import os
from database.core.storage.sqlite.sqlite_service import SQLiteService


@pytest.fixture
def db():
    """Create a temporary SQLite DB with test data."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT, amount REAL, status TEXT)"
    )
    conn.executemany(
        "INSERT INTO test (name, amount, status) VALUES (?, ?, ?)",
        [
            ("Alice", 100.0, "active"),
            ("Bob", 200.0, "active"),
            ("Charlie", 50.0, "inactive"),
            ("Diana", 150.0, "pending"),
        ],
    )
    conn.commit()
    conn.close()

    service = SQLiteService(db_path=path)
    yield service

    service.close()
    os.unlink(path)


def test_query_equal(db):
    rows = db.query("test", conditions=[("name", "=", "Alice")])
    assert len(rows) == 1
    assert rows[0]["name"] == "Alice"
    assert rows[0]["amount"] == 100.0


def test_query_not_equal(db):
    rows = db.query("test", conditions=[("status", "!=", "active")])
    assert len(rows) == 2
    names = {r["name"] for r in rows}
    assert names == {"Charlie", "Diana"}


def test_query_greater_than(db):
    rows = db.query("test", conditions=[("amount", ">", 75)])
    assert len(rows) == 3
    names = {r["name"] for r in rows}
    assert names == {"Alice", "Bob", "Diana"}


def test_query_less_than(db):
    rows = db.query("test", conditions=[("amount", "<", 100)])
    assert len(rows) == 1
    assert rows[0]["name"] == "Charlie"


def test_query_greater_equal(db):
    rows = db.query("test", conditions=[("amount", ">=", 150)])
    assert len(rows) == 2
    names = {r["name"] for r in rows}
    assert names == {"Bob", "Diana"}


def test_query_less_equal(db):
    rows = db.query("test", conditions=[("amount", "<=", 100)])
    assert len(rows) == 2
    names = {r["name"] for r in rows}
    assert names == {"Alice", "Charlie"}


def test_query_like(db):
    rows = db.query("test", conditions=[("name", "like", "Ali")])
    assert len(rows) == 1
    assert rows[0]["name"] == "Alice"


def test_query_like_partial(db):
    rows = db.query("test", conditions=[("name", "like", "li")])
    assert len(rows) == 2


def test_query_in(db):
    rows = db.query("test", conditions=[("status", "in", ["active", "pending"])])
    assert len(rows) == 3


def test_query_between(db):
    rows = db.query("test", conditions=[("amount", "between", [80, 160])])
    assert len(rows) == 2


def test_count_all(db):
    assert db.count("test") == 4


def test_count_with_conditions(db):
    assert db.count("test", [("status", "=", "active")]) == 2


def test_sum_all(db):
    assert db.sum("test", "amount") == 500.0


def test_sum_with_conditions(db):
    assert db.sum("test", "amount", [("status", "=", "active")]) == 300.0


def test_insert(db):
    new_id = db.insert("test", {"name": "Eve", "amount": 300.0, "status": "active"})
    assert new_id > 0
    assert db.count("test") == 5


def test_insert_many(db):
    count = db.insert_many(
        "test",
        [
            {"name": "Frank", "amount": 10.0, "status": "active"},
            {"name": "Grace", "amount": 20.0, "status": "inactive"},
        ],
    )
    assert count == 2
    assert db.count("test") == 6


def test_execute_raw(db):
    rows = db.execute("SELECT * FROM test WHERE amount > ?", [100])
    assert len(rows) == 2


def test_query_order_by(db):
    rows = db.query("test", order_by="amount DESC", limit=2)
    assert len(rows) == 2
    assert rows[0]["amount"] == 200.0
    assert rows[1]["amount"] == 150.0


def test_query_columns(db):
    rows = db.query("test", columns=["name", "status"])
    assert set(rows[0].keys()) == {"name", "status"}


def test_field_mapping(db):
    rows = db.query("test", conditions=[("amount_total", "=", 100.0)])
    assert len(rows) == 1
    assert rows[0]["name"] == "Alice"
""",

    # 6. Test: AuditRegistry
    "tests/unit/test_audit_registry.py": """"""Tests for AuditRegistry — Registry Pattern."""

import pytest
from database.core.audits.registry.audit_registry import AuditRegistry, AuditInfo


@pytest.fixture
def registry():
    return AuditRegistry()


def test_registry_has_all_default_audits(registry):
    audits = registry.list_audits()
    assert len(audits) == 10


def test_registry_contains_missing_receipts(registry):
    assert "missing_receipts" in registry.list_audits()


def test_registry_contains_refunds(registry):
    assert "refunds" in registry.list_audits()


def test_registry_contains_daily_summary(registry):
    assert "daily_summary" in registry.list_audits()


def test_registry_contains_monthly_summary(registry):
    assert "monthly_summary" in registry.list_audits()


def test_registry_contains_sales_summary(registry):
    assert "sales_summary" in registry.list_audits()


def test_registry_contains_payment_methods(registry):
    assert "payment_methods" in registry.list_audits()


def test_registry_contains_cashier_performance(registry):
    assert "cashier_performance" in registry.list_audits()


def test_registry_contains_session(registry):
    assert "session" in registry.list_audits()


def test_registry_contains_business_unit_kpi(registry):
    assert "business_unit_kpi" in registry.list_audits()


def test_registry_contains_category_ranking(registry):
    assert "category_ranking" in registry.list_audits()


def test_get_existing_audit(registry):
    info = registry.get("missing_receipts")
    assert info is not None
    assert isinstance(info, AuditInfo)
    assert info.code == "MISSING_RCPT"
    assert info.name == "missing_receipts"


def test_get_audit_with_description(registry):
    info = registry.get("cashier_performance")
    assert info.description == "Cashier performance KPI"


def test_get_nonexistent_audit(registry):
    assert registry.get("nonexistent_audit") is None


def test_register_new_audit(registry):
    new_audit = AuditInfo(
        name="custom_audit",
        code="CUSTOM",
        description="A custom test audit",
        module_path="tests.dummy",
    )
    registry.register(new_audit)
    assert "custom_audit" in registry.list_audits()
    assert registry.get("custom_audit").code == "CUSTOM"


def test_list_by_category_pos(registry):
    pos_audits = registry.list_audits(category="pos")
    assert len(pos_audits) == 10


def test_list_by_category_empty(registry):
    empty = registry.list_audits(category="accounting")
    assert len(empty) == 0


def test_all_audits_have_codes(registry):
    for name, info in registry.list_audits().items():
        assert info.code, f"Audit {name} missing code"
        assert info.module_path, f"Audit {name} missing module_path"


def test_all_audits_have_descriptions(registry):
    for name, info in registry.list_audits().items():
        assert info.description, f"Audit {name} missing description"
""",

    # 7. Test: ContextBuilder
    "tests/unit/test_context_builder.py": """"""Tests for AuditContextBuilder and related dataclasses."""

import pytest
from unittest.mock import MagicMock
from datetime import datetime
from database.core.context.context_builder import (
    AuditContextBuilder,
    AuditContext,
    BusinessUnit,
    SessionContext,
)


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


def test_build_with_session_id():
    mock_sqlite = MagicMock()
    mock_sqlite.query.side_effect = [
        [{"id": 5, "name": "Session 5", "business_unit_id": 2, "state": "closed"}],
        [{"id": 2, "name": "Branch B", "company_id": 1}],
    ]

    builder = AuditContextBuilder(sqlite_service=mock_sqlite)
    ctx = builder.build(session_id=5)

    assert ctx.session is not None
    assert ctx.session.id == 5
    assert ctx.session.name == "Session 5"
    assert ctx.business_unit is not None
    assert ctx.business_unit.id == 2


def test_build_with_date_range():
    mock_sqlite = MagicMock()
    builder = AuditContextBuilder(sqlite_service=mock_sqlite)
    ctx = builder.build(date_from="2026-01-01", date_to="2026-12-31")

    assert ctx.date_from == "2026-01-01"
    assert ctx.date_to == "2026-12-31"
    assert ctx.business_unit is None


def test_build_from_session_map():
    mock_sqlite = MagicMock()
    mock_sqlite.query.side_effect = [
        [{"session_id": 10, "business_unit_id": 3}],
        [{"id": 3, "name": "Branch C", "company_id": 1}],
        [{"id": 10, "name": "Session 10", "state": "opened"}],
    ]

    builder = AuditContextBuilder(sqlite_service=mock_sqlite)
    ctx = builder.build_from_session_map(session_id=10)

    assert ctx.business_unit is not None
    assert ctx.business_unit.id == 3
    assert ctx.session is not None
    assert ctx.session.id == 10


def test_build_business_unit_not_found():
    mock_sqlite = MagicMock()
    mock_sqlite.query.return_value = []

    builder = AuditContextBuilder(sqlite_service=mock_sqlite)
    ctx = builder.build(business_unit_id=999)

    assert ctx.business_unit is None
""",

    # 8. Test: RefundSpikeAudit
    "tests/unit/test_refund_spike.py": """"""Tests for RefundSpikeAudit."""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from database.core.audits.refunds.refund_spike_audit import RefundSpikeAudit


@pytest.fixture
def audit():
    with patch("database.core.audits.refunds.refund_spike_audit.SQLiteDatabase") as MockDB:
        instance = RefundSpikeAudit()
        instance._db = MockDB.return_value
        yield instance


def test_no_refunds_today(audit):
    audit.get_orders = MagicMock(return_value=[])
    audit._db.query.return_value = [{"count": 0, "amount": 0}]

    result = audit.analyze()

    assert result["today_refunds"] == 0
    assert result["today_amount"] == 0.0
    assert result["risk_level"] == "LOW"
    assert result["spike_ratio"] == 0.0


def test_normal_refund_rate(audit):
    audit.get_orders = MagicMock(return_value=[])
    audit._db.query.return_value = [{"count": 30, "amount": 3000.0}]

    result = audit.analyze()

    assert result["daily_avg_refunds"] == 1.0
    assert result["risk_level"] == "LOW"


def test_medium_risk_spike(audit):
    today = datetime.now().strftime("%Y-%m-%d")
    audit.get_orders = MagicMock(return_value=[
        {"id": 1, "amount_total": -50, "date_order": f"{today} 10:00:00", "user_id": 5, "name": "Order 001"},
        {"id": 2, "amount_total": -60, "date_order": f"{today} 11:00:00", "user_id": 5, "name": "Order 002"},
        {"id": 3, "amount_total": -40, "date_order": f"{today} 12:00:00", "user_id": 6, "name": "Order 003"},
    ])
    audit._db.query.return_value = [{"count": 45, "amount": 4500.0}]

    result = audit.analyze()

    assert result["today_refunds"] == 3
    assert result["today_amount"] == 150.0
    assert result["spike_ratio"] == 2.0
    assert result["risk_level"] == "MEDIUM"


def test_high_risk_spike(audit):
    today = datetime.now().strftime("%Y-%m-%d")
    audit.get_orders = MagicMock(return_value=[
        {"id": i, "amount_total": -100, "date_order": f"{today} 10:00:00", "user_id": 10, "name": f"Order {i}"}
        for i in range(10)
    ])
    audit._db.query.return_value = [{"count": 30, "amount": 3000.0}]

    result = audit.analyze()

    assert result["today_refunds"] == 10
    assert result["today_amount"] == 1000.0
    assert result["spike_ratio"] == 10.0
    assert result["risk_level"] == "HIGH"


def test_top_cashiers(audit):
    today = datetime.now().strftime("%Y-%m-%d")
    audit.get_orders = MagicMock(return_value=[
        {"id": 1, "amount_total": -50, "date_order": f"{today} 10:00:00", "user_id": 5, "name": "O1"},
        {"id": 2, "amount_total": -60, "date_order": f"{today} 11:00:00", "user_id": 5, "name": "O2"},
        {"id": 3, "amount_total": -40, "date_order": f"{today} 12:00:00", "user_id": 6, "name": "O3"},
        {"id": 4, "amount_total": -30, "date_order": f"{today} 13:00:00", "user_id": 6, "name": "O4"},
        {"id": 5, "amount_total": -20, "date_order": f"{today} 14:00:00", "user_id": 7, "name": "O5"},
    ])
    audit._db.query.return_value = [{"count": 30, "amount": 3000.0}]

    result = audit.analyze()

    assert len(result["top_cashiers"]) == 3
    assert result["top_cashiers"][0]["cashier_id"] == 5
    assert result["top_cashiers"][0]["refund_count"] == 2


def test_top_refunds_sorted(audit):
    today = datetime.now().strftime("%Y-%m-%d")
    audit.get_orders = MagicMock(return_value=[
        {"id": 1, "amount_total": -500, "date_order": f"{today} 10:00:00", "user_id": 1, "name": "Big Refund"},
        {"id": 2, "amount_total": -50, "date_order": f"{today} 11:00:00", "user_id": 2, "name": "Small Refund"},
    ])
    audit._db.query.return_value = [{"count": 30, "amount": 3000.0}]

    result = audit.analyze()

    assert len(result["top_refunds"]) == 2
    assert result["top_refunds"][0]["amount"] == 500.0
    assert result["top_refunds"][1]["amount"] == 50.0


def test_amount_spike_high_risk(audit):
    today = datetime.now().strftime("%Y-%m-%d")
    audit.get_orders = MagicMock(return_value=[
        {"id": 1, "amount_total": -5000, "date_order": f"{today} 10:00:00", "user_id": 1, "name": "O1"},
    ])
    audit._db.query.return_value = [{"count": 30, "amount": 3000.0}]

    result = audit.analyze()

    assert result["amount_spike"] == 50.0
    assert result["risk_level"] == "HIGH"


def test_audit_code_and_name(audit):
    assert audit.code == "refund_spike"
    assert audit.name == "Refund Spike Detection"
""",

    # 9. Test: BaseRepository (fixed)
    "tests/unit/test_base_repository.py": """"""Tests for BaseRepository — fixed to work with SQLiteService."""

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
    repo.service.conn = None

    yield repo

    repo.service.close()
    os.unlink(path)


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


def test_count_all(repo):
    assert repo.count() == 4


def test_count_with_domain(repo):
    assert repo.count(domain=[("active", "=", 0)]) == 1


def test_count_no_match(repo):
    assert repo.count(domain=[("price", ">", 100)]) == 0
""",
}

OLD_TESTS = [
    "tests/unit/test_ai_context.py",
    "tests/unit/test_query_parser.py",
    "tests/unit/test_sql_builder.py",
    "tests/unit/test_sql_executor.py",
]


def main():
    print("=" * 60)
    print("  Odoo AI Audit Platform — Auto-Install Script")
    print("=" * 60)

    # 1. Remove old dummy tests
    print("\n🗑️  Removing old dummy tests...")
    for old_test in OLD_TESTS:
        path = PROJECT_ROOT / old_test
        if path.exists():
            path.unlink()
            print(f"   ✓ Removed: {old_test}")
        else:
            print(f"   ⚠ Already gone: {old_test}")

    # 2. Write all new/updated files
    print("\n📝 Writing new files...")
    for rel_path, content in FILES.items():
        full_path = PROJECT_ROOT / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Backup existing file
        if full_path.exists():
            backup = full_path.with_suffix(full_path.suffix + ".backup")
            shutil.copy2(full_path, backup)
            print(f"   💾 Backed up: {rel_path}")

        full_path.write_text(content, encoding="utf-8")
        print(f"   ✓ Written: {rel_path}")

    # 3. Run pytest
    print("\n🧪 Running pytest...")
    os.chdir(PROJECT_ROOT)
    exit_code = os.system("python -m pytest tests/unit/ -v")

    print("\n" + "=" * 60)
    if exit_code == 0:
        print("  ✅ All tests passed!")
    else:
        print(f"  ⚠️  pytest exited with code {exit_code}")
    print("=" * 60)


if __name__ == "__main__":
    main()
