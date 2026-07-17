from database.query.query_analyzer import QueryAnalyzer
from database.planner.query_planner import QueryPlanner
from database.services.metadata_cache import MetadataCache


def test_product_filter_planning():

    cache = MetadataCache()
    cache.load()

    product = cache.products[0]["name"]

    analyzer = QueryAnalyzer(metadata_cache=cache)
    planner = QueryPlanner()

    analysis = analyzer.analyze(
        f"show sales for {product}"
    )

    plan = planner.plan(analysis)

    assert "product_id = %s" in plan["where"]
