"""
Query Analyzer

Architecture V7

Combines all NLP extractors into one semantic analysis.
"""

from __future__ import annotations

from database.ai.intent.intent_classifier import IntentClassifier
from database.ai.intent.entity_extractor import EntityExtractor
from database.ai.intent.aggregate_extractor import AggregateExtractor
from database.ai.intent.operator_extractor import OperatorExtractor
from database.ai.intent.value_extractor import ValueExtractor
from database.ai.intent.date_extractor import DateExtractor


class QueryAnalyzer:

    def __init__(self):

        self.intent = IntentClassifier()
        self.entities = EntityExtractor()
        self.aggregates = AggregateExtractor()
        self.operators = OperatorExtractor()
        self.values = ValueExtractor()
        self.dates = DateExtractor()

    # ---------------------------------------------------------

    def analyze(self, text: str):

        intent = self.intent.classify(text)

        return {
            "intent": intent.intent,
            "confidence": intent.confidence,
            "entities": self.entities.extract(text),
            "aggregate": self.aggregates.extract(text),
            "operator": self.operators.extract(text),
            "value": self.values.extract(text),
            "date": self.dates.extract(text),
        }
