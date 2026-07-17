from database.formatter.result_formatter import ResultFormatter


def test_format_table():

    formatter = ResultFormatter()

    result = formatter.format(
        ["id", "name"],
        [
            (1, "Invoice 1"),
        ],
    )

    assert result["count"] == 1
    assert result["rows"][0]["id"] == 1
    assert result["rows"][0]["name"] == "Invoice 1"
