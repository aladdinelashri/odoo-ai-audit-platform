from database.results.result_formatter import ResultFormatter


def test_empty():
    formatter = ResultFormatter()

    result = formatter.format([], [])

    assert result == []


def test_one_row():
    formatter = ResultFormatter()

    columns = [
        "id",
        "name",
    ]

    rows = [
        (1, "Invoice 001"),
    ]

    result = formatter.format(columns, rows)

    assert result == [
        {
            "id": 1,
            "name": "Invoice 001",
        }
    ]


def test_multiple_rows():
    formatter = ResultFormatter()

    columns = [
        "id",
        "state",
    ]

    rows = [
        (1, "posted"),
        (2, "draft"),
    ]

    result = formatter.format(columns, rows)

    assert result == [
        {
            "id": 1,
            "state": "posted",
        },
        {
            "id": 2,
            "state": "draft",
        },
    ]


def test_single_column():
    formatter = ResultFormatter()

    columns = [
        "count",
    ]

    rows = [
        (15,),
    ]

    result = formatter.format(columns, rows)

    assert result == [
        {
            "count": 15,
        }
    ]


def test_sum():
    formatter = ResultFormatter()

    columns = [
        "total",
    ]

    rows = [
        (2500.75,),
    ]

    result = formatter.format(columns, rows)

    assert result == [
        {
            "total": 2500.75,
        }
    ]
