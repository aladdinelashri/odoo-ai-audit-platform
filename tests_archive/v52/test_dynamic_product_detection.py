from database.query.query_analyzer import QueryAnalyzer
from database.services.metadata_cache import MetadataCache


def test_dynamic_product_detection():

    cache = MetadataCache()
    cache.load()

    product_name = cache.products[0]["name"]

    analyzer = QueryAnalyzer(metadata_cache=cache)

    analysis = analyzer.analyze(
        f"show sales for {product_name}"
    )

    assert analysis["product"]["name"] == product_name
