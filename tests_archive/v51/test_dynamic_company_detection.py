from database.query.query_analyzer import QueryAnalyzer
from database.services.metadata_cache import MetadataCache


def test_dynamic_company_detection():

    cache = MetadataCache()
    cache.load()

    analyzer = QueryAnalyzer(metadata_cache=cache)

    analysis = analyzer.analyze("show invoices for جمعية مصر الجديدة")

    assert analysis["company"]["name"] == "جمعية مصر الجديدة"
