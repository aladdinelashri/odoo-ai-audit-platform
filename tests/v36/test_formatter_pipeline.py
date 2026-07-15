from database.formatter.result_formatter import ResultFormatter


def test_formatter_pipeline():

    formatter = ResultFormatter()

    result = formatter.format(
        ["id", "name"],
        [
            (1, "Invoice 1"),
            (2, "Invoice 2"),
        ],
    )

    assert result["count"] == 2
    assert result["rows"][1]["name"] == "Invoice 2"
