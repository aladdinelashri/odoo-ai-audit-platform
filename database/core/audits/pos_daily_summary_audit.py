from database.core.audits.base.base_pos_audit import BasePOSAudit


class POSDailySummaryAudit(BasePOSAudit):

    code = "pos_daily_summary"

    name = "POS Daily Summary Audit"

    def analyze(self):

        orders = self.get_orders(
            domain=[
                ("state", "=", "paid"),
            ],
            fields=[
                "id",
                "date_order",
                "amount_total",
                "company_id",
                "session_id",
                "name",
            ],
            order="date_order",
        )

        summary = {}

        for order in orders:

            context = self.build_context(order)

            if context.business_unit is None:
                continue

            day = order["date_order"][:10]

            key = (
                context.company_id,
                context.business_unit.id,
                day,
            )

            if key not in summary:

                summary[key] = {
                    "company_id": context.company_id,
                    "business_unit_id": context.business_unit.id,
                    "business_unit_name": context.business_unit.name,
                    "date": day,
                    "orders": 0,
                    "sales": 0.0,
                }

            summary[key]["orders"] += 1
            summary[key]["sales"] += order["amount_total"]

        return list(summary.values())
