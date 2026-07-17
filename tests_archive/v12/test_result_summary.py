from database.results.result_summary import ResultSummary


def test_empty():

    summary = ResultSummary()

    result = summary.summarize([])

    assert result == {
        "count": 0,
        "empty": True,
    }


def test_one():

    summary = ResultSummary()

    rows = [
        {
            "id": 1,
        }
    ]

    result = summary.summarize(rows)

    assert result == {
        "count": 1,
        "empty": False,
    }


def test_many():

    summary = ResultSummary()

    rows = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
        {"id": 5},
    ]

    result = summary.summarize(rows)

    assert result["count"] == 5
    assert result["empty"] is False


def test_invoice_rows():

    summary = ResultSummary()

    rows = [
        {"name": "INV001"},
        {"name": "INV002"},
    ]

    result = summary.summarize(rows)

    assert result["count"] == 2


def test_boolean():

    summary = ResultSummary()

    result = summary.summarize([{"x": 1}])

    assert result["empty"] is False
