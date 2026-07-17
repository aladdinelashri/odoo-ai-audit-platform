"""
Query Analyzer

Architecture V51
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

    DATE_FILTERS = {
        "today": "today",
        "yesterday": "yesterday",
        "this month": "this_month",
        "this year": "this_year",
    }

    def __init__(self, metadata_cache=None):

        self.metadata_cache = metadata_cache

    def analyze(self, query: str) -> dict:

        query_lower = query.lower()
        words = query_lower.split()

        intent = None
        aggregation = None
        entities = []
        filters = []

        company = None
        journal = None
        partner = None
        product = None
        warehouse = None
        pos_config = None

        # ------------------------------------

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

                value = self.FILTERS[word]

                if value not in filters:
                    filters.append(value)

        # ------------------------------------

        for phrase, value in self.DATE_FILTERS.items():

            if phrase in query_lower:

                if value not in filters:
                    filters.append(value)

        # ------------------------------------
        # Dynamic metadata detection
        # ------------------------------------

        if self.metadata_cache is not None:

            for item in self.metadata_cache.companies:

                name = item.get("name")

                if name and name.lower() in query_lower:
                    company = item
                    break

            for item in self.metadata_cache.journals:

                name = item.get("name")

                if name and name.lower() in query_lower:
                    journal = item
                    break

            for item in self.metadata_cache.products:

                name = item.get("name")

                if name and name.lower() in query_lower:
                    product = item
                    break

            for item in self.metadata_cache.partners:

                name = item.get("name")

                if name and name.lower() in query_lower:
                    partner = item
                    break

            for item in self.metadata_cache.warehouses:

                name = item.get("name")

                if name and name.lower() in query_lower:
                    warehouse = item
                    break

            for item in self.metadata_cache.pos_configs:

                name = item.get("name")

                if name and name.lower() in query_lower:
                    pos_config = item
                    break

        # ------------------------------------

        return {
            "query": query,
            "intent": intent,
            "aggregation": aggregation,
            "entities": entities,
            "filters": filters,
            "company": company,
            "journal": journal,
            "partner": partner,
            "product": product,
            "warehouse": warehouse,
            "pos_config": pos_config,
        }
