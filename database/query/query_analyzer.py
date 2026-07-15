"""
Query Analyzer

Architecture V32
"""

from __future__ import annotations


class QueryAnalyzer:

    INTENTS = {
        "show": "show",
        "list": "show",
        "display": "show",
        "find": "show",
        "get": "show",
    }

    AGGREGATIONS = {
        "count": "count",
        "sum": "sum",
        "total": "sum",
        "average": "average",
        "avg": "average",
    }

    ENTITIES = {
        "invoice": "invoice",
        "invoices": "invoice",
        "customer": "customer",
        "customers": "customer",
        "partner": "partner",
        "partners": "partner",
        "product": "product",
        "products": "product",
        "journal": "journal",
        "journals": "journal",
        "order": "order",
        "orders": "order",
        "pos": "pos",
    }

    FILTERS = {
        "unpaid": "unpaid",
        "paid": "paid",
        "posted": "posted",
        "draft": "draft",
        "cancelled": "cancelled",
    }

    def analyze(self, query: str) -> dict:

        words = query.lower().split()

        intent = None
        aggregation = None
        entities = []
        filters = []

        for word in words:

            if intent is None and word in self.INTENTS:
                intent = self.INTENTS[word]

            if aggregation is None and word in self.AGGREGATIONS:
                aggregation = self.AGGREGATIONS[word]

            if word in self.ENTITIES:
                entity = self.ENTITIES[word]
                if entity not in entities:
                    entities.append(entity)

            if word in self.FILTERS:
                filter_name = self.FILTERS[word]
                if filter_name not in filters:
                    filters.append(filter_name)

        return {
            "query": query,
            "intent": intent,
            "aggregation": aggregation,
            "entities": entities,
            "filters": filters,
        }
