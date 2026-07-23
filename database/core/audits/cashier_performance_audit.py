# database/core/audits/cashier_performance_audit.py

from database.core.audits.base.base_pos_audit import BasePOSAudit
from database.core.storage.sqlite.database import SQLiteDatabase


class CashierPerformanceAudit(BasePOSAudit):

    code = "cashier_performance"
    name = "Cashier Performance Audit"

    def __init__(self):
        super().__init__()
        self._db = SQLiteDatabase()

    def analyze(self):
        """
        Analyze session performance for each business unit.
        Uses session_id as grouping key with session_name.
        Includes payment methods analysis.
        """

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

            # Use session_id as grouping key
            session_id = order.get("session_id")
            if isinstance(session_id, list):
                session_id = session_id[0] if session_id else None

            if not session_id:
                continue

            # Get session name from database
            session_name = self.get_session_name(session_id)

            key = (
                context.company_id,
                context.business_unit.id,
                session_id,
            )

            if key not in summary:
                summary[key] = {
                    "company_id": context.company_id,
                    "business_unit_id": context.business_unit.id,
                    "business_unit_name": context.business_unit.name,
                    "session_id": session_id,
                    "session_name": session_name,
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

            refund_rate = (total_refunds / total_orders * 100) if total_orders > 0 else 0.0

            avg_sale = total_sales / total_orders if total_orders > 0 else 0.0
            
            payment_methods = data["payment_methods"]
            payment_method_totals = data["payment_method_totals"]
            
            top_payment_method = None
            if payment_method_totals:
                top_payment_method = max(payment_method_totals, key=payment_method_totals.get)

            result.append({
                "company_id": data["company_id"],
                "business_unit_id": data["business_unit_id"],
                "business_unit_name": data["business_unit_name"],
                "session_id": data["session_id"],
                "session_name": data["session_name"],
                "number_of_orders": total_orders,
                "total_sales": round(total_sales, 2),
                "average_sale": round(avg_sale, 2),
                "number_of_refunds": total_refunds,
                "refund_amount": round(refund_amount, 2),
                "refund_rate_percent": round(refund_rate, 2),
                "net_sales": round(net_sales, 2),
                "number_of_payment_methods": len(payment_methods),
                "top_payment_method": top_payment_method,
            })

        # Sort by business_unit_id, then by sales desc
        result.sort(key=lambda x: (x["business_unit_id"], -x["total_sales"]))

        return result

    def get_session_name(self, session_id):
        """
        Fetch session_name from pos_sessions table.
        """
        rows = self._db.query(
            """
            SELECT
                session_name
            FROM pos_sessions
            WHERE id = ?
            """,
            (session_id,)
        )
        if rows:
            return rows[0]["session_name"] if rows[0]["session_name"] else f"Session {session_id}"
        return f"Session {session_id}"
