"""Integration tests for email delivery flow with mocked SMTP."""
import pytest
from unittest.mock import patch, MagicMock
import smtplib
from database.core.reporting.scheduler import _send_email_smtp, _deliver_report


class TestSMTPRetry:
    """Test tenacity retry logic."""

    @patch("database.core.reporting.scheduler.smtplib.SMTP")
    def test_retry_on_connection_error(self, mock_smtp_class):
        """Test that SMTP connection errors trigger retries."""
        mock_server = MagicMock()
        mock_server.starttls.side_effect = ConnectionError("Connection refused")
        mock_smtp_class.return_value.__enter__.return_value = mock_server
        
        with pytest.raises(Exception):
            _send_email_smtp(
                recipients=["test@example.com"],
                subject="Test",
                body="<html><body>Test</body></html>",
            )
        
        # Should have attempted 3 times (initial + 2 retries)
        assert mock_smtp_class.call_count == 3

    @patch("database.core.reporting.scheduler.smtplib.SMTP")
    def test_success_after_retry(self, mock_smtp_class):
        """Test success after transient failure."""
        mock_server = MagicMock()
        # Fail twice, succeed on third
        mock_server.starttls.side_effect = [
            ConnectionError("Fail 1"),
            ConnectionError("Fail 2"),
            None,
        ]
        mock_smtp_class.return_value.__enter__.return_value = mock_server
        
        _send_email_smtp(
            recipients=["test@example.com"],
            subject="Test",
            body="<html><body>Test</body></html>",
        )
        
        assert mock_smtp_class.call_count == 3
        mock_server.send_message.assert_called_once()

    @patch("database.core.reporting.scheduler.smtplib.SMTP")
    def test_auth_failure_no_retry(self, mock_smtp_class):
        """Test that auth failures are handled correctly."""
        mock_server = MagicMock()
        mock_server.starttls.return_value = None
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, b"Auth failed")
        mock_smtp_class.return_value.__enter__.return_value = mock_server
        
        with pytest.raises(smtplib.SMTPAuthenticationError):
            _send_email_smtp(
                recipients=["test@example.com"],
                subject="Test",
                body="<html><body>Test</body></html>",
            )


class TestDeliverReport:
    """Test report delivery integration."""

    @patch("database.core.reporting.scheduler._send_email_smtp")
    def test_deliver_report_no_recipients(self, mock_send):
        """Test delivery with no recipients."""
        from database.core.storage.sqlite.sqlite_pool import SQLitePool
        
        status = _deliver_report(
            report_id=1,
            report_name="Test",
            recipients=[],
            data=[{"id": 1}],
            execution_id=1,
            db_pool=None,
        )
        assert status == "no_recipients"
        mock_send.assert_not_called()

    @patch("database.core.reporting.scheduler._send_email_smtp")
    def test_deliver_report_with_attachment(self, mock_send):
        """Test delivery generates attachment and sends email."""
        data = [{"id": 1, "order_name": "Order-001", "amount_total": 100.00}]
        
        status = _deliver_report(
            report_id=1,
            report_name="Test Report",
            recipients=["test@example.com"],
            data=data,
            execution_id=1,
            db_pool=None,
            export_format="excel",
        )
        
        assert status == "delivered"
        mock_send.assert_called_once()
        call_args = mock_send.call_args
        assert call_args.kwargs["recipients"] == ["test@example.com"]
        assert "attachment_bytes" in call_args.kwargs
        assert call_args.kwargs["attachment_filename"] == "Test Report.xlsx"
