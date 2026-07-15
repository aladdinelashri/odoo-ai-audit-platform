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

        table = None

        if entities:
            table = self.MODEL_MAP.get(entities[0])

        postgres_table = (
            table.replace(".", "_")
            if table
            else None
        )

        where = []
        params = []

        for filter_name in analysis.get("filters", []):

            if filter_name == "unpaid":
                where.append("payment_state = %s")
                params.append("not_paid")

            elif filter_name == "paid":
                where.append("payment_state = %s")
                params.append("paid")

            elif filter_name == "posted":
                where.append("state = %s")
                params.append("posted")

            elif filter_name == "draft":
                where.append("state = %s")
                params.append("draft")

            elif filter_name == "cancelled":
                where.append("state = %s")
                params.append("cancel")

        return {
            # Business information
            "model": table,
            "operation": analysis.get("intent"),
            "aggregation": analysis.get("aggregation"),
            "filters": analysis.get("filters", []),

            # SQL execution plan
            "table": table,
            "select": ["*"],
            "from": postgres_table,
            "where": where,
            "where_values": params,
            "params": params,
            "order": [],
            "limit": None,
        }
