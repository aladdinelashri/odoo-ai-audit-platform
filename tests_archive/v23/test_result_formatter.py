from database.formatter.result_formatter import ResultFormatter


def test_format_simple_rows():

    formatter = ResultFormatter()

    columns = ["id", "name", "state"]

    rows = [
        (1, "INV/001", "posted"),
        (2, "INV/002", "draft"),
    ]

    result = formatter.format(columns, rows)

    assert result["count"] == 2

    assert result["columns"] == columns

    assert result["rows"][0]["id"] == 1

    assert result["rows"][0]["name"] == "INV/001"

    assert result["rows"][1]["state"] == "draft"
