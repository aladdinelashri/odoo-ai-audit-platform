from database.discovery.discovery_engine import DiscoveryEngine


def test_empty_entity_list():

    engine = DiscoveryEngine()

    result = engine.discover("show invoices")

    assert "entities" in result
    assert isinstance(result["entities"], list)
