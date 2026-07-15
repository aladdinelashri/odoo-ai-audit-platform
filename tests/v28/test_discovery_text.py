from database.discovery.discovery_engine import DiscoveryEngine


def test_original_text_preserved():

    engine = DiscoveryEngine()

    query = "show invoices"

    result = engine.discover(query)

    assert result["text"] == query
