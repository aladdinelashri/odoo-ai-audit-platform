"""
Core Query Parser

Architecture V3
"""

from __future__ import annotations

from database.core.pipeline.context import PipelineContext

from database.ai.intent_detector import IntentDetector
from database.ai.entity_detector import EntityDetector
from database.ai.parameter_detector import ParameterDetector
from database.ai.filter_detector import FilterDetector


class QueryParser:

    def __init__(self):

        self.intent_detector = IntentDetector()
        self.entity_detector = EntityDetector()
        self.parameter_detector = ParameterDetector()
        self.filter_detector = FilterDetector()

    # ---------------------------------------------------------

    def parse(self, context):

        if isinstance(context, str):
            text = context
            pipeline_context = None
        else:
            text = context.query
            pipeline_context = context

        parameters = self.parameter_detector.detect(text)

        parsed = {

            "query": text,

            "intent": self.intent_detector.detect(text),

            "entities": self.entity_detector.detect(text),

            "parameters": parameters,

            "filters": self.filter_detector.detect(text),

            "aggregate": parameters.get("aggregate"),

        }

        if pipeline_context is not None:
            pipeline_context.parsed = parsed

        return parsed
