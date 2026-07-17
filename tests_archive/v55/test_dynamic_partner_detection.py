from database.query.query_analyzer import QueryAnalyzer
from database.services.metadata_cache import MetadataCache


def test_dynamic_partner_detection():

    cache = MetadataCache()
    cache.load()

    partner = next(
        p for p in cache.partners
        if p["name"]
    )

    analyzer = QueryAnalyzer(metadata_cache=cache)

    analysis = analyzer.analyze(
        f"show invoices for {partner['name']}"
    )

    assert analysis["partner"]["name"] == partner["name"]
