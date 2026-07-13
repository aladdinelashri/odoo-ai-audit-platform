from database.core.pipeline.context import PipelineContext
from database.core.response.response_formatter import ResponseFormatter


def test_response_is_dict():

    context = PipelineContext("show invoices")

    context.rows = [{"id": 1}, {"id": 2}]

    result = ResponseFormatter().format(context)

    assert isinstance(result, dict)


def test_response_success():

    context = PipelineContext("show invoices")

    context.rows = [{"id": 1}]

    result = ResponseFormatter().format(context)

    assert result["success"] is True


def test_response_count():

    context = PipelineContext("show invoices")

    context.rows = [{"id": 1}, {"id": 2}, {"id": 3}]

    result = ResponseFormatter().format(context)

    assert result["count"] == 3
