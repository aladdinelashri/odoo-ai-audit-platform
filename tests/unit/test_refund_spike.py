"""Tests for RefundSpikeAudit."""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from database.core.audits.refunds.refund_spike_audit import RefundSpikeAudit


@pytest.fixture
def audit():
    """Create a RefundSpikeAudit with mocked dependencies."""
    with patch("database.core.audits.refunds.refund_spike_audit.SQLiteDatabase") as MockDB:
        instance = RefundSpikeAudit()
        instance._db = MockDB.return_value
        yield instance


# ─── No refunds today ───
def test_no_refunds_today(audit):
    audit.get_orders = MagicMock(return_value=[])
    audit._db.query.return_value = [{"count": 0, "amount": 0}]

    result = audit.analyze()

    assert result["today_refunds"] == 0
    assert result["today_amount"] == 0.0
    assert result["risk_level"] == "LOW"
    assert result["spike_ratio"] == 0.0


# ─── Normal refund rate (below threshold) ───
def test_normal_refund_rate(audit):
    audit.get_orders = MagicMock(return_value=[])
    # 30 refunds over 30 days = 1/day average
    audit._db.query.return_value = [{"count": 30, "amount": 3000.0}]

    result = audit.analyze()

    assert result["daily_avg_refunds"] == 1.0
    assert result["risk_level"] == "LOW"


# ─── MEDIUM risk: 200% spike ───
def test_medium_risk_spike(audit):
    today = datetime.now().strftime("%Y-%m-%d")
    audit.get_orders = MagicMock(return_value=[
        {"id": 1, "amount_total": -50, "date_order": f"{today} 10:00:00", "user_id": 5, "name": "Order 001"},
        {"id": 2, "amount_total": -60, "date_order": f"{today} 11:00:00", "user_id": 5, "name": "Order 002"},
        {"id": 3, "amount_total": -40, "date_order": f"{today} 12:00:00", "user_id": 6, "name": "Order 003"},
    ])
    # 45 refunds over 30 days = 1.5/day average
    # Today: 3 refunds → spike_ratio = 3 / 1.5 = 2.0 → MEDIUM
    audit._db.query.return_value = [{"count": 45, "amount": 4500.0}]

    result = audit.analyze()

    assert result["today_refunds"] == 3
    assert result["today_amount"] == 150.0
    assert result["spike_ratio"] == 2.0
    assert result["risk_level"] == "MEDIUM"


# ─── HIGH risk: 300% spike ───
def test_high_risk_spike(audit):
    today = datetime.now().strftime("%Y-%m-%d")
    audit.get_orders = MagicMock(return_value=[
        {"id": i, "amount_total": -100, "date_order": f"{today} 10:00:00", "user_id": 10, "name": f"Order {i}"}
        for i in range(10)
    ])
    # 30 refunds over 30 days = 1/day average
    # Today: 10 refunds → spike_ratio = 10 / 1 = 10.0 → HIGH
    audit._db.query.return_value = [{"count": 30, "amount": 3000.0}]

    result = audit.analyze()

    assert result["today_refunds"] == 10
    assert result["today_amount"] == 1000.0
    assert result["spike_ratio"] == 10.0
    assert result["risk_level"] == "HIGH"


# ─── Top cashiers tracked ───
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
    assert result["top_cashiers"][0]["cashier_id"] == 5  # 2 refunds
    assert result["top_cashiers"][0]["refund_count"] == 2


# ─── Top refunds by amount ───
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


# ─── Amount spike triggers HIGH risk ───
def test_amount_spike_high_risk(audit):
    today = datetime.now().strftime("%Y-%m-%d")
    audit.get_orders = MagicMock(return_value=[
        {"id": 1, "amount_total": -5000, "date_order": f"{today} 10:00:00", "user_id": 1, "name": "O1"},
    ])
    # 30 refunds over 30 days = 1/day, $100/day average
    # Today: $5000 → amount_spike = 5000 / 100 = 50.0 → HIGH
    audit._db.query.return_value = [{"count": 30, "amount": 3000.0}]

    result = audit.analyze()

    assert result["amount_spike"] == 50.0
    assert result["risk_level"] == "HIGH"


# ─── Audit metadata ───
def test_audit_code_and_name(audit):
    assert audit.code == "refund_spike"
    assert audit.name == "Refund Spike Detection"
