from database.response.result_formatter import ResultFormatter


def test_format_rows():

    formatter = ResultFormatter()

    result = formatter.format(
        [
            {"id": 1, "name": "A"},
            {"id": 2, "name": "B"},
        ]
    )

    assert result["count"] == 2
    assert len(result["rows"]) == 2
