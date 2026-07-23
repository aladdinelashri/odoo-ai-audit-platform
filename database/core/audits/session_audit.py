# database/core/audits/session_audit.py

from database.core.audits.base.base_pos_audit import BasePOSAudit
from database.core.storage.sqlite.database import SQLiteDatabase


class SessionAudit(BasePOSAudit):

    code = "session_audit"
    name = "Session Audit"

    def __init__(self):
        super().__init__()
        self._db = SQLiteDatabase()

    def analyze(self):
        """
        Audit POS sessions: totals, payments.
        Limited to available columns: id, config_id, session_name
        """
        
        sessions = self._db.query(
            """
            SELECT 
                ps.id,
                ps.session_name,
                ps.config_id,
                pc.name as config_name
            FROM pos_sessions ps
            LEFT JOIN pos_configs pc ON ps.config_id = pc.id
            ORDER BY ps.id DESC
            """
        )

        result = []

        for session in sessions:
            
            session_id = session["id"]
            
            order_stats = self.get_order_stats(session_id)
            payment_stats = self.get_payment_stats(session_id)
            
            result.append({
                "session_id": session_id,
                "session_name": session["session_name"] or f"Session {session_id}",
                "config_name": session["config_name"] or "Unknown",
                "orders_count": order_stats["count"],
                "total_sales": round(order_stats["sales"], 2),
                "total_payments": round(payment_stats["total"], 2),
                "cash_sales": round(payment_stats.get("cash", 0.0), 2),
                "bank_sales": round(payment_stats.get("bank", 0.0), 2),
                "card_sales": round(payment_stats.get("card", 0.0), 2),
            })

        return result

    def get_order_stats(self, session_id):
        """
        Get order statistics for a session.
        """
        rows = self._db.query(
            """
            SELECT 
                COUNT(*) as count,
                COALESCE(SUM(amount_total), 0.0) as sales
            FROM pos_orders
            WHERE session_id = ? AND state = 'paid'
            """,
            (session_id,)
        )
        
        if rows:
            return {
                "count": rows[0]["count"] or 0,
                "sales": rows[0]["sales"] or 0.0,
            }
        
        return {"count": 0, "sales": 0.0}

    def get_payment_stats(self, session_id):
        """
        Get payment statistics for a session.
        """
        rows = self._db.query(
            """
            SELECT 
                payment_method,
                COALESCE(SUM(amount), 0.0) as total
            FROM pos_payments
            WHERE session_id = ?
            GROUP BY payment_method
            """,
            (session_id,)
        )
        
        stats = {"total": 0.0}
        
        for row in rows:
            method = row["payment_method"] or "unknown"
            amount = row["total"] or 0.0
            stats[method.lower()] = amount
            stats["total"] += amount
        
        return stats
