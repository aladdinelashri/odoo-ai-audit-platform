from database.query.query_analyzer import QueryAnalyzer
from database.services.metadata_cache import MetadataCache


def test_dynamic_warehouse_detection():

    cache = MetadataCache()
    cache.load()

    warehouse_name = cache.warehouses[0]["name"]

    analyzer = QueryAnalyzer(metadata_cache=cache)

    analysis = analyzer.analyze(
        f"show stock in {warehouse_name}"
    )

    assert analysis["warehouse"]["name"] == warehouse_name
