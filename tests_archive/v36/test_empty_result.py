from database.formatter.result_formatter import ResultFormatter


def test_empty_result():

    formatter = ResultFormatter()

    result = formatter.format(
        ["id", "name"],
        [],
    )

    assert result["count"] == 0
    assert result["rows"] == []
