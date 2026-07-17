from database.query.query_analyzer import QueryAnalyzer
from database.services.metadata_cache import MetadataCache


def test_dynamic_pos_detection():

    cache = MetadataCache()
    cache.load()

    pos_name = cache.pos_configs[0]["name"]

    analyzer = QueryAnalyzer(metadata_cache=cache)

    analysis = analyzer.analyze(
        f"show sales for {pos_name}"
    )

    assert analysis["pos_config"]["name"] == pos_name
