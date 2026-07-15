"""
Query Planner

Architecture V33
"""

from __future__ import annotations


class QueryPlanner:

    MODEL_MAP = {
        "invoice": "account.move",
        "customer": "res.partner",
        "partner": "res.partner",
        "product": "product.template",
        "journal": "account.journal",
        "order": "pos.order",
        "pos": "pos.order",
    }

    def plan(self, analysis: dict) -> dict:

        entities = analysis.get("entities", [])

        model = None

        if entities:
            model = self.MODEL_MAP.get(entities[0])

        return {
            "model": model,
            "operation": analysis.get("intent"),
            "aggregation": analysis.get("aggregation"),
            "filters": analysis.get("filters", []),
        }
