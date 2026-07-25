#!/bin/bash
# Odoo AI Audit Platform - Auto-Install Script
# Run: bash install_audit_updates.sh

set -e

cd /home/helioit/odoo-ai-audit-platform 2>/dev/null || cd "$(dirname "$0")"

echo "============================================================"
echo "  Odoo AI Audit Platform - Auto-Install"
echo "============================================================"

# 1. Remove old dummy tests
echo ""
echo "Removing old dummy tests..."
rm -f tests/unit/test_ai_context.py tests/unit/test_query_parser.py tests/unit/test_sql_builder.py tests/unit/test_sql_executor.py
echo "   Done."

# 2. Fix BaseRepository
echo ""
echo "Fixing BaseRepository..."
cat > database/core/repositories/base_repository.py << 'PYEOF'
"""Base repository backed by SQLite cache."""

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
        """Search records matching domain."""
        return self.service.query(
            table=self.TABLE,
            columns=fields,
            conditions=domain,
            order_by=order,
            limit=limit,
        )

    def read(self, ids, fields=None):
        """Read records by IDs."""
        if not ids:
            return []
        id_list = ids if isinstance(ids, (list, tuple)) else [ids]
        return self.service.query(
            table=self.TABLE,
            columns=fields,
            conditions=[("id", "in", id_list)],
        )

    def count(self, domain=None):
        """Count records matching domain."""
        return self.service.count(
            table=self.TABLE,
            conditions=domain,
        )
PYEOF
echo "   Written: database/core/repositories/base_repository.py"

# 3. Fix AuditRegistry
echo ""
echo "Fixing AuditRegistry..."
cat > database/core/audits/registry/audit_registry.py << 'PYEOF'
"""
Audit Registry - Registry Pattern for all audit modules.
Central registry to dynamically discover and run audits.
"""

import importlib
import logging
from typing import Dict, Callable, Any, Optional
from dataclasses import dataclass

from config.logging import get_logger

logger = get_logger("audit.registry")


@dataclass
class AuditInfo:
    """Metadata for a registered audit."""
    name: str
    code: str
    description: str
    module_path: str
    func_name: str = "run"
    category: str = "pos"


class AuditRegistry:
    """Central registry for all audit modules."""

    def __init__(self):
        self._audits: Dict[str, AuditInfo] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register all built-in audits."""
        defaults = [
            AuditInfo("missing_receipts", "MISSING_RCPT", "Detect missing receipts", "database.core.audits.missing_receipts_audit"),
            AuditInfo("refunds", "REFUNDS", "Analyze refund patterns", "database.core.audits.refunds.refund_spike_audit"),
            AuditInfo("daily_summary", "DAILY_SUM", "Daily POS summary", "database.core.audits.pos_daily_summary_audit"),
            AuditInfo("monthly_summary", "MONTHLY_SUM", "Monthly POS summary", "database.core.audits.pos_monthly_summary_audit"),
            AuditInfo("sales_summary", "SALES_SUM", "Sales performance summary", "database.core.audits.pos_sales_summary_audit"),
            AuditInfo("payment_methods", "PAY_METH", "Payment method breakdown", "database.core.audits.payment_method_summary_audit"),
            AuditInfo("cashier_performance", "CASH_PERF", "Cashier performance KPI", "database.core.audits.cashier_performance_audit"),
            AuditInfo("session", "SESSION", "POS session audit", "database.core.audits.session_audit"),
            AuditInfo("business_unit_kpi", "BU_KPI", "Business unit KPI", "database.core.audits.business_unit_kpi_audit"),
            AuditInfo("category_ranking", "CAT_RANK", "Category daily ranking", "database.core.audits.pos_category_daily_ranking_audit"),
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
        """Dynamically load and run an audit by name."""
        audit = self.get(name)
        if not audit:
            raise ValueError(f"Audit '{name}' not found. Available: {list(self._audits.keys())}")
        try:
            module = importlib.import_module(audit.module_path)
            func = getattr(module, audit.func_name, None)
            if not func:
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if callable(attr) and not attr_name.startswith("_"):
                        func = attr
                        break
            if not func:
                raise AttributeError(f"No callable found in {audit.module_path}")
            logger.info(f"Running audit: {audit.name} ({audit.code})")
            return func(context, **kwargs)
        except Exception as e:
            logger.error(f"Failed to run audit '{name}': {e}")
            raise


registry = AuditRegistry()
PYEOF
echo "   Written: database/core/audits/registry/audit_registry.py"

# 4. Update refunds/__init__.py
echo ""
echo "Updating refunds/__init__.py..."
mkdir -p database/core/audits/refunds
cat > database/core/audits/refunds/__init__.py << 'PYEOF'
"""Refund audit modules."""

from database.core.audits.refunds.refund_audit import RefundAudit
from database.core.audits.refunds.refund_spike_audit import RefundSpikeAudit

__all__ = ["RefundAudit", "RefundSpikeAudit"]
PYEOF
echo "   Written: database/core/audits/refunds/__init__.py"

# 5. Create RefundSpikeAudit
echo ""
echo "Creating RefundSpikeAudit..."
cat > database/core/audits/refunds/refund_spike_audit.py << 'PYEOF'
"""Refund Spike Detection - flags abnormal refund patterns."""

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
        """Analyze refund patterns and detect anomalies."""
        today = datetime.now().strftime("%Y-%m-%d")

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

        spike_ratio = (today_count / daily_avg) if daily_avg > 0 else 0.0
        amount_spike = (today_amount / daily_avg_amount) if daily_avg_amount > 0 else 0.0

        risk = "LOW"
        if spike_ratio > 2.8 or amount_spike > 2.8:
            risk = "HIGH"
        elif spike_ratio > 1.5 or amount_spike > 1.5:
            risk = "MEDIUM"

        cashiers = Counter(o.get("user_id", "Unknown") for o in today_refunds)
        top_cashiers = [
            {"cashier_id": c, "refund_count": n}
            for c, n in cashiers.most_common(5)
        ]

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
PYEOF
echo "   Written: database/core/audits/refunds/refund_spike_audit.py"

# 6. Test: SQLiteService
echo ""
echo "Creating test_sqlite_service.py..."
cat > tests/unit/test_sqlite_service.py << 'PYEOF'
"""Tests for SQLiteService - full operator coverage."""

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
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT, amount REAL, status TEXT)")
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


def test_query_not_equal(db):
    rows = db.query("test", conditions=[("status", "!=", "active")])
    assert len(rows) == 2


def test_query_greater_than(db):
    rows = db.query("test", conditions=[("amount", ">", 75)])
    assert len(rows) == 3


def test_query_less_than(db):
    rows = db.query("test", conditions=[("amount", "<", 100)])
    assert len(rows) == 1


def test_query_greater_equal(db):
    rows = db.query("test", conditions=[("amount", ">=", 150)])
    assert len(rows) == 2


def test_query_less_equal(db):
    rows = db.query("test", conditions=[("amount", "<=", 100)])
    assert len(rows) == 2


def test_query_like(db):
    rows = db.query("test", conditions=[("name", "like", "Ali")])
    assert len(rows) == 1


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


def test_field_mapping(db):
    rows = db.query("test", conditions=[("amount_total", "=", 100.0)])
    assert len(rows) == 1
    assert rows[0]["name"] == "Alice"
PYEOF
echo "   Written: tests/unit/test_sqlite_service.py"

# 7. Test: AuditRegistry
echo ""
echo "Creating test_audit_registry.py..."
cat > tests/unit/test_audit_registry.py << 'PYEOF'
"""Tests for AuditRegistry - Registry Pattern."""

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


def test_get_existing_audit(registry):
    info = registry.get("missing_receipts")
    assert info is not None
    assert isinstance(info, AuditInfo)
    assert info.code == "MISSING_RCPT"


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
PYEOF
echo "   Written: tests/unit/test_audit_registry.py"

# 8. Test: ContextBuilder
echo ""
echo "Creating test_context_builder.py..."
cat > tests/unit/test_context_builder.py << 'PYEOF'
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


def test_business_unit_from_row():
    row = {"id": 5, "name": "Downtown Branch", "company_id": 1, "code": "DT001"}
    bu = BusinessUnit.from_row(row)
    assert bu.id == 5
    assert bu.name == "Downtown Branch"
    assert bu.company_id == 1


def test_business_unit_from_row_defaults():
    row = {"id": 1}
    bu = BusinessUnit.from_row(row)
    assert bu.name == "Unknown"
    assert bu.company_id is None


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
    assert d["date_from"] == "2026-07-01"


def test_build_with_business_unit_id():
    mock_sqlite = MagicMock()
    mock_sqlite.query.return_value = [
        {"id": 1, "name": "Main Branch", "company_id": 1}
    ]
    builder = AuditContextBuilder(sqlite_service=mock_sqlite)
    ctx = builder.build(business_unit_id=1)
    assert ctx.business_unit is not None
    assert ctx.business_unit.id == 1


def test_build_with_date_range():
    mock_sqlite = MagicMock()
    builder = AuditContextBuilder(sqlite_service=mock_sqlite)
    ctx = builder.build(date_from="2026-01-01", date_to="2026-12-31")
    assert ctx.date_from == "2026-01-01"
    assert ctx.business_unit is None


def test_build_business_unit_not_found():
    mock_sqlite = MagicMock()
    mock_sqlite.query.return_value = []
    builder = AuditContextBuilder(sqlite_service=mock_sqlite)
    ctx = builder.build(business_unit_id=999)
    assert ctx.business_unit is None
PYEOF
echo "   Written: tests/unit/test_context_builder.py"

# 9. Test: RefundSpikeAudit
echo ""
echo "Creating test_refund_spike.py..."
cat > tests/unit/test_refund_spike.py << 'PYEOF'
"""Tests for RefundSpikeAudit."""

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
    assert result["risk_level"] == "LOW"


def test_medium_risk_spike(audit):
    today = datetime.now().strftime("%Y-%m-%d")
    audit.get_orders = MagicMock(return_value=[
        {"id": 1, "amount_total": -50, "date_order": f"{today} 10:00:00", "user_id": 5, "name": "O1"},
        {"id": 2, "amount_total": -60, "date_order": f"{today} 11:00:00", "user_id": 5, "name": "O2"},
        {"id": 3, "amount_total": -40, "date_order": f"{today} 12:00:00", "user_id": 6, "name": "O3"},
    ])
    audit._db.query.return_value = [{"count": 45, "amount": 4500.0}]
    result = audit.analyze()
    assert result["today_refunds"] == 3
    assert result["spike_ratio"] == 2.0
    assert result["risk_level"] == "MEDIUM"


def test_high_risk_spike(audit):
    today = datetime.now().strftime("%Y-%m-%d")
    audit.get_orders = MagicMock(return_value=[
        {"id": i, "amount_total": -100, "date_order": f"{today} 10:00:00", "user_id": 10, "name": f"O{i}"}
        for i in range(10)
    ])
    audit._db.query.return_value = [{"count": 30, "amount": 3000.0}]
    result = audit.analyze()
    assert result["today_refunds"] == 10
    assert result["spike_ratio"] == 10.0
    assert result["risk_level"] == "HIGH"


def test_top_cashiers(audit):
    today = datetime.now().strftime("%Y-%m-%d")
    audit.get_orders = MagicMock(return_value=[
        {"id": 1, "amount_total": -50, "date_order": f"{today} 10:00", "user_id": 5, "name": "O1"},
        {"id": 2, "amount_total": -60, "date_order": f"{today} 11:00", "user_id": 5, "name": "O2"},
        {"id": 3, "amount_total": -40, "date_order": f"{today} 12:00", "user_id": 6, "name": "O3"},
    ])
    audit._db.query.return_value = [{"count": 30, "amount": 3000.0}]
    result = audit.analyze()
    assert len(result["top_cashiers"]) == 2
    assert result["top_cashiers"][0]["cashier_id"] == 5


def test_audit_code_and_name(audit):
    assert audit.code == "refund_spike"
    assert audit.name == "Refund Spike Detection"
PYEOF
echo "   Written: tests/unit/test_refund_spike.py"

# 10. Test: BaseRepository
echo ""
echo "Creating test_base_repository.py..."
cat > tests/unit/test_base_repository.py << 'PYEOF'
"""Tests for BaseRepository - fixed to work with SQLiteService."""

import pytest
import sqlite3
import tempfile
import os
from database.core.repositories.base_repository import BaseRepository


class TestRepository(BaseRepository):
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


def test_search_with_limit(repo):
    rows = repo.search(limit=2)
    assert len(rows) == 2


def test_search_with_order(repo):
    rows = repo.search(order="price DESC")
    assert rows[0]["name"] == "Date"


def test_read_single_id(repo):
    rows = repo.read(1)
    assert len(rows) == 1
    assert rows[0]["name"] == "Apple"


def test_read_multiple_ids(repo):
    rows = repo.read([1, 2])
    assert len(rows) == 2


def test_count_all(repo):
    assert repo.count() == 4


def test_count_with_domain(repo):
    assert repo.count(domain=[("active", "=", 0)]) == 1
PYEOF
echo "   Written: tests/unit/test_base_repository.py"

# 11. Run pytest
echo ""
echo "============================================================"
echo "Running pytest..."
python -m pytest tests/unit/ -v

EXIT_CODE=$?

echo ""
echo "============================================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "  All tests passed!"
else
    echo "  pytest exited with code $EXIT_CODE"
fi
echo "============================================================"
