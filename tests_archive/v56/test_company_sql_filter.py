from database.query.query_analyzer import QueryAnalyzer
from database.planner.query_planner import QueryPlanner
from database.services.metadata_cache import MetadataCache


def test_company_filter_planning():

    cache = MetadataCache()
    cache.load()

    company = cache.companies[0]["name"]

    analyzer = QueryAnalyzer(metadata_cache=cache)
    planner = QueryPlanner()

    analysis = analyzer.analyze(
        f"show invoices for {company}"
    )

    plan = planner.plan(analysis)

    assert "company_id" in str(plan)
