from database.discovery.discovery_engine import DiscoveryEngine


def test_discovery_engine_creation():

    engine = DiscoveryEngine()

    assert engine is not None
