"""
Query Planner

Architecture V61
"""

from __future__ import annotations

from database.metadata.model_registry import ModelRegistry


class QueryPlanner:

    def __init__(self, model_registry: ModelRegistry | None = None):

        self.model_registry = model_registry or ModelRegistry()

    def plan(self, analysis: dict) -> dict:

        entities = analysis.get("entities", [])

        table = None

        if entities:
            table = self.model_registry.get_model(entities[0])

        postgres_table = (
            table.replace(".", "_")
            if table
            else None
        )

        where = []
        params = []

        company = analysis.get("company")

        if company is not None:
            where.append("company_id = %s")
            params.append(company["id"])

        journal = analysis.get("journal")

        if journal is not None:
            where.append("journal_id = %s")
            params.append(journal["id"])

        partner = analysis.get("partner")

        if partner is not None:
            where.append("partner_id = %s")
            params.append(partner["id"])

        product = analysis.get("product")

        if product is not None:
            where.append("product_id = %s")
            params.append(product["id"])

        warehouse = analysis.get("warehouse")

        if warehouse is not None:
            where.append("warehouse_id = %s")
            params.append(warehouse["id"])

        pos_config = analysis.get("pos_config")

        if pos_config is not None:
            where.append("config_id = %s")
            params.append(pos_config["id"])

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

            elif filter_name == "today":
                where.append("invoice_date = CURRENT_DATE")

            elif filter_name == "yesterday":
                where.append(
                    "invoice_date = CURRENT_DATE - INTERVAL '1 day'"
                )

            elif filter_name == "this_month":
                where.append(
                    "invoice_date >= DATE_TRUNC('month', CURRENT_DATE)"
                )

            elif filter_name == "this_year":
                where.append(
                    "invoice_date >= DATE_TRUNC('year', CURRENT_DATE)"
                )

        return {
            "model": table,
            "operation": analysis.get("intent"),
            "aggregation": analysis.get("aggregation"),
            "filters": analysis.get("filters", []),
            "table": table,
            "select": ["*"],
            "from": postgres_table,
            "where": where,
            "where_values": params,
            "params": params,
            "order": [],
            "limit": None,
        }
