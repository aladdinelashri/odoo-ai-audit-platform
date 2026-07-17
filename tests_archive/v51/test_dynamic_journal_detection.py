from database.query.query_analyzer import QueryAnalyzer
from database.services.metadata_cache import MetadataCache


def test_dynamic_journal_detection():

    cache = MetadataCache()
    cache.load()

    journal_name = cache.journals[0]["name"]

    analyzer = QueryAnalyzer(metadata_cache=cache)

    analysis = analyzer.analyze(
        f"show invoices from {journal_name}"
    )

    assert analysis["journal"]["name"] == journal_name
