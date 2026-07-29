import pytest
from unittest.mock import patch, MagicMock
from database.core.discovery.odoo_discovery import OdooModelDiscovery


def test_retry_on_failure():
    """Verify that the discovery retries on failure."""
    mock_conn = MagicMock()
    mock_conn.search_read.side_effect = [
        Exception("Connection error"),
        Exception("Timeout"),
        [{"id": 1, "name": "Test"}]
    ]

    # Instantiate the class (takes no arguments) and inject the mock client
    discovery = OdooModelDiscovery()
    discovery.client = mock_conn

    with patch("time.sleep", return_value=None):
        result = discovery.discover_fields("account.move")

    assert result is not None
    assert mock_conn.search_read.call_count == 3
