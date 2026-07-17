from database.formatter.result_formatter import ResultFormatter


def test_summary_format():

    formatter = ResultFormatter()

    result = formatter.format(
        ["id"],
        [
            (1,),
            (2,),
            (3,),
        ],
    )

    assert result["count"] == 3
