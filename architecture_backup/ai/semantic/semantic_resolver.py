"""
Semantic Resolver

Architecture V5

Unified access point for all semantic dictionaries.
"""

from __future__ import annotations

from database.ai.semantic.model_dictionary import ModelDictionary
from database.ai.semantic.field_dictionary import FieldDictionary
from database.ai.semantic.aggregate_dictionary import AggregateDictionary
from database.ai.semantic.operator_dictionary import OperatorDictionary
from database.ai.semantic.value_dictionary import ValueDictionary


class SemanticResolver:

    def __init__(self) -> None:

        self.models = ModelDictionary()
        self.fields = FieldDictionary()
        self.aggregates = AggregateDictionary()
        self.operators = OperatorDictionary()
        self.values = ValueDictionary()

    def resolve_model(self, text):
        return self.models.resolve(text)

    def resolve_field(self, text):
        return self.fields.resolve(text)

    def resolve_aggregate(self, text):
        return self.aggregates.resolve(text)

    def resolve_operator(self, text):
        return self.operators.resolve(text)

    def resolve_value(self, text):
        return self.values.resolve(text)
