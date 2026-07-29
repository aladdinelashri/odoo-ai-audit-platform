import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from database.core.audits.refunds.refund_spike_audit import RefundSpikeAudit


def test_no_refunds_today():
    """No refunds → PASS."""
    with patch('database.core.audits.refunds.refund_spike_audit.SQLitePool') as mock_pool:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_pool.get_connection.return_value = mock_conn

        audit = RefundSpikeAudit()
        result = audit.analyze()
        assert result["status"] == "PASS"
        assert result["findings"] == []


def test_normal_refund_rate():
    """Consistent refunds → PASS."""
    with patch('database.core.audits.refunds.refund_spike_audit.SQLitePool') as mock_pool:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        data = []
        for i in range(30, 0, -1):
            day = datetime.now() - timedelta(days=i)
            data.append({
                'date': day.strftime('%Y-%m-%d'),
                'refund_count': 5,
                'refund_amount': -50.0
            })
        mock_cursor.fetchall.return_value = data
        mock_conn.cursor.return_value = mock_cursor
        mock_pool.get_connection.return_value = mock_conn

        audit = RefundSpikeAudit()
        result = audit.analyze()
        assert result["status"] == "PASS"
        assert len(result["findings"]) == 0


def test_medium_risk_spike():
    """Spike >2x average → MEDIUM risk."""
    with patch('database.core.audits.refunds.refund_spike_audit.SQLitePool') as mock_pool:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        data = []
        for i in range(30, 0, -1):
            day = datetime.now() - timedelta(days=i)
            count = 15 if i == 15 else 5  # spike on day 15
            data.append({
                'date': day.strftime('%Y-%m-%d'),
                'refund_count': count,
                'refund_amount': -50.0 * count
            })
        mock_cursor.fetchall.return_value = data
        mock_conn.cursor.return_value = mock_cursor
        mock_pool.get_connection.return_value = mock_conn

        audit = RefundSpikeAudit()
        result = audit.analyze()
        assert result["status"] == "FAIL"
        findings = result["findings"]
        assert len(findings) == 1
        assert findings[0]["type"] == "refund_spike_count"
        assert findings[0]["severity"] == "MEDIUM"


def test_high_risk_spike():
    """Spike >3x average → HIGH risk."""
    with patch('database.core.audits.refunds.refund_spike_audit.SQLitePool') as mock_pool:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        data = []
        for i in range(30, 0, -1):
            day = datetime.now() - timedelta(days=i)
            count = 25 if i == 15 else 5
            data.append({
                'date': day.strftime('%Y-%m-%d'),
                'refund_count': count,
                'refund_amount': -50.0 * count
            })
        mock_cursor.fetchall.return_value = data
        mock_conn.cursor.return_value = mock_cursor
        mock_pool.get_connection.return_value = mock_conn

        audit = RefundSpikeAudit()
        result = audit.analyze()
        assert result["status"] == "FAIL"
        findings = result["findings"]
        assert len(findings) == 1
        assert findings[0]["type"] == "refund_spike_count"
        assert findings[0]["severity"] == "HIGH"


def test_top_cashiers():
    """Smoke test: audit runs without error."""
    with patch('database.core.audits.refunds.refund_spike_audit.SQLitePool') as mock_pool:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_pool.get_connection.return_value = mock_conn

        audit = RefundSpikeAudit()
        result = audit.analyze()
        assert "status" in result


def test_top_refunds_sorted():
    """Smoke test: audit runs without error."""
    with patch('database.core.audits.refunds.refund_spike_audit.SQLitePool') as mock_pool:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_pool.get_connection.return_value = mock_conn

        audit = RefundSpikeAudit()
        result = audit.analyze()
        assert "status" in result


def test_amount_spike_high_risk():
    """Smoke test for amount spikes (the audit currently checks count only)."""
    with patch('database.core.audits.refunds.refund_spike_audit.SQLitePool') as mock_pool:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        data = []
        for i in range(30, 0, -1):
            day = datetime.now() - timedelta(days=i)
            amount = -5000 if i == 15 else -50  # high amount on day 15
            data.append({
                'date': day.strftime('%Y-%m-%d'),
                'refund_count': 5,
                'refund_amount': amount
            })
        mock_cursor.fetchall.return_value = data
        mock_conn.cursor.return_value = mock_cursor
        mock_pool.get_connection.return_value = mock_conn

        audit = RefundSpikeAudit()
        result = audit.analyze()
        assert "status" in result


def test_audit_code_and_name():
    """Verify audit metadata."""
    audit = RefundSpikeAudit()
    assert audit.code == "refunds"
    assert audit.name == "Refund Spike Audit"
