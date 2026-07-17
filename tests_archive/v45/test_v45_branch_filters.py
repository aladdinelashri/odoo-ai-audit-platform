import pytest

from database.query.query_analyzer import QueryAnalyzer
from database.services.metadata_cache import MetadataCache


def test_company_detection():

    cache = MetadataCache()
    cache.load()

    if not cache.companies:
        pytest.skip("No companies found")

    company = cache.companies[0]["name"]

    analyzer = QueryAnalyzer(metadata_cache=cache)

    analysis = analyzer.analyze(
        f"show invoices for {company}"
    )

    assert analysis["company"] is not None
