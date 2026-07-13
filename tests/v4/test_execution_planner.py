from database.core.pipeline.context import PipelineContext
from database.core.ai.query_parser import QueryParser
from database.core.planner.execution_planner import ExecutionPlanner


def test_execution_plan():

    parser = QueryParser()
    planner = ExecutionPlanner()

    context = PipelineContext("show invoices")

    parser.parse(context)

    plan = planner.build(context)

    assert plan["success"] is True


def test_execution_has_table():

    parser = QueryParser()
    planner = ExecutionPlanner()

    context = PipelineContext("show invoices")

    parser.parse(context)

    plan = planner.build(context)

    assert "table" in plan


def test_execution_has_fields():

    parser = QueryParser()
    planner = ExecutionPlanner()

    context = PipelineContext("show invoices")

    parser.parse(context)

    plan = planner.build(context)

    assert isinstance(plan["fields"], list)
