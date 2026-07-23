# database/core/audits/pos_daily_summary_audit.py

from database.core.audits.base.base_pos_audit import BasePOSAudit
from database.core.storage.sqlite.database import SQLiteDatabase


class POSDailySummaryAudit(BasePOSAudit):

    code = "pos_daily_summary"
    name = "POS Daily Summary Audit"

    def __init__(self):
        super().__init__()
        self._db = SQLiteDatabase()

    def analyze(self):

        # ⚡ OPTIMIZATION: Load all payments once
        all_payments = self._db.query(
            "SELECT order_id, payment_method, amount FROM pos_payments"
        )
        
        payments_by_order = {}
        for p in all_payments:
            oid = p["order_id"]
            if oid not in payments_by_order:
                payments_by_order[oid] = []
            payments_by_order[oid].append(p)

        orders = self.get_orders(
            domain=[
                ("state", "=", "done"),  # ✅ تعديل: "done" بدلاً من "paid"
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
                    "refunds": 0,
                    "refund_amount": 0.0,
                    "payment_methods": set(),
                    "payment_method_totals": {},
                }

            amount = order.get("amount_total", 0.0) or 0.0
            
            if amount < 0:
                summary[key]["refunds"] += 1
                summary[key]["refund_amount"] += abs(amount)
            else:
                summary[key]["orders"] += 1
                summary[key]["sales"] += amount

            # ⚡ OPTIMIZATION: Use memory instead of SQL query
            payments = payments_by_order.get(order["id"], [])
            for payment in payments:
                method = payment["payment_method"] if payment["payment_method"] else "Unknown"
                
                summary[key]["payment_methods"].add(method)
                
                if method not in summary[key]["payment_method_totals"]:
                    summary[key]["payment_method_totals"][method] = 0.0
                summary[key]["payment_method_totals"][method] += payment["amount"] if payment["amount"] else 0.0

        result = []
        for key, data in summary.items():
            
            total_orders = data["orders"]
            total_sales = data["sales"]
            total_refunds = data["refunds"]
            refund_amount = data["refund_amount"]
            
            net_sales = total_sales - refund_amount
            
            avg_order_value = total_sales / total_orders if total_orders > 0 else 0.0
            
            payment_methods = data["payment_methods"]
            payment_method_totals = data["payment_method_totals"]
            
            top_payment_method = None
            if payment_method_totals:
                top_payment_method = max(payment_method_totals, key=payment_method_totals.get)
            
            result.append({
                "company_id": data["company_id"],
                "business_unit_id": data["business_unit_id"],
                "business_unit_name": data["business_unit_name"],
                "date": data["date"],
                "orders": total_orders,
                "sales": round(total_sales, 2),
                "average_order_value": round(avg_order_value, 2),
                "refunds": total_refunds,
                "refund_amount": round(refund_amount, 2),
                "net_sales": round(net_sales, 2),
                "number_of_payment_methods": len(payment_methods),
                "top_payment_method": top_payment_method,
            })

        # Sort by date desc, then business_unit_id
        result.sort(key=lambda x: (x["date"], x["business_unit_id"]), reverse=True)
        
        return result
