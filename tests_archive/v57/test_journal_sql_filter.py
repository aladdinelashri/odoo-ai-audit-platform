from database.query.query_analyzer import QueryAnalyzer
from database.planner.query_planner import QueryPlanner
from database.services.metadata_cache import MetadataCache


def test_journal_filter_planning():

    cache = MetadataCache()
    cache.load()

    journal = cache.journals[0]["name"]

    analyzer = QueryAnalyzer(metadata_cache=cache)
    planner = QueryPlanner()

    analysis = analyzer.analyze(
        f"show invoices from {journal}"
    )

    plan = planner.plan(analysis)

    assert "journal_id = %s" in plan["where"]
