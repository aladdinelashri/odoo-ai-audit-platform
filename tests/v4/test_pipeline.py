from database.core.pipeline.pipeline import Pipeline


def test_pipeline_show_invoices():

    pipeline = Pipeline()

    result = pipeline.run("show invoices")

    assert result["success"] is True


def test_pipeline_count():

    pipeline = Pipeline()

    result = pipeline.run("count invoices")

    assert result["success"] is True


def test_pipeline_sql_exists():

    pipeline = Pipeline()

    result = pipeline.run("show invoices")

    assert "sql" in result
