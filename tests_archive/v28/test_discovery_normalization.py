from database.discovery.discovery_engine import DiscoveryEngine


def test_query_normalization():

    engine = DiscoveryEngine()

    result = engine.discover("  SHOW   Invoices  ")

    assert result["text"].strip().lower() == "show   invoices"
