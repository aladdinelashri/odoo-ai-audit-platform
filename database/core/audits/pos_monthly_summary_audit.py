# database/core/audits/pos_monthly_summary_audit.py

from database.core.audits.base.base_pos_audit import BasePOSAudit
from database.core.storage.sqlite.database import SQLiteDatabase


class POSMonthlySummaryAudit(BasePOSAudit):

    code = "pos_monthly_summary"
    name = "POS Monthly Summary Audit"

    def __init__(self):
        super().__init__()
        self._db = SQLiteDatabase()

    def analyze(self):
        """
        Produce a reusable monthly aggregation for each month × business unit.
        Includes payment methods analysis.
        """
        
        orders = self.get_orders(
            domain=[
                ("state", "=", "paid"),
            ],
            fields=[
                "id",
                "amount_total",
                "company_id",
                "session_id",
                "name",
                "date_order",
            ],
            order="date_order",
        )

        summary = {}

        for order in orders:
            
            context = self.build_context(order)
            
            if context.business_unit is None:
                continue

            order_date = order.get("date_order", "")
            if not order_date:
                continue
            
            if isinstance(order_date, str):
                month = order_date[:7]
            else:
                month = order_date.strftime("%Y-%m")

            key = (
                month,
                context.company_id,
                context.business_unit.id,
            )

            if key not in summary:
                summary[key] = {
                    "month": month,
                    "company_id": context.company_id,
                    "business_unit_id": context.business_unit.id,
                    "business_unit_name": context.business_unit.name,
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

            # Get payments for this order
            payments = self.get_payments_for_order(order["id"])
            for payment in payments:
                # sqlite3.Row — استخدام [] بدلاً من .get()
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
                "month": data["month"],
                "company_id": data["company_id"],
                "business_unit_id": data["business_unit_id"],
                "business_unit_name": data["business_unit_name"],
                "number_of_orders": total_orders,
                "total_sales": round(total_sales, 2),
                "average_order_value": round(avg_order_value, 2),
                "number_of_refunds": total_refunds,
                "refund_amount": round(refund_amount, 2),
                "net_sales": round(net_sales, 2),
                "number_of_payment_methods": len(payment_methods),
                "top_payment_method": top_payment_method,
            })

        result.sort(key=lambda x: (x["month"], x["business_unit_id"]), reverse=True)
        
        return result

    def get_payments_for_order(self, order_id):
        """
        Fetch payments for a specific POS order.
        """
        rows = self._db.query(
            """
            SELECT 
                payment_method,
                amount
            FROM pos_payments
            WHERE order_id = ?
            """,
            (order_id,)
        )
        return rows
