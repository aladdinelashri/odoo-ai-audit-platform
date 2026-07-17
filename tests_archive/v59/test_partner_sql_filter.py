from database.query.query_analyzer import QueryAnalyzer
from database.planner.query_planner import QueryPlanner
from database.services.metadata_cache import MetadataCache


def test_partner_filter_planning():

    cache = MetadataCache()
    cache.load()

    partner = next(
        p for p in cache.partners
        if p["name"]
    )["name"]

    analyzer = QueryAnalyzer(metadata_cache=cache)
    planner = QueryPlanner()

    analysis = analyzer.analyze(
        f"show invoices for {partner}"
    )

    plan = planner.plan(analysis)

    assert "partner_id = %s" in plan["where"]
