from database.core.pipeline.pipeline import Pipeline


def test_count_invoices():

    pipeline = Pipeline()

    result = pipeline.run("count invoices")

    assert result["success"] is True

    assert result["count"] == 1

    assert "value" in result


def test_sum_invoices():

    pipeline = Pipeline()

    result = pipeline.run("sum invoices")

    assert result["success"] is True

    assert "value" in result


def test_average_invoice_amount():

    pipeline = Pipeline()

    result = pipeline.run("average invoice amount")

    assert result["success"] is True

    assert "value" in result
