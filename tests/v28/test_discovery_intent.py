from database.discovery.discovery_engine import DiscoveryEngine


def test_intent_key_exists():

    engine = DiscoveryEngine()

    result = engine.discover("show invoices")

    assert "intent" in result
