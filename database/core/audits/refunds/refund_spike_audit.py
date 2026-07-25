"""Refund Spike Detection — flags abnormal refund patterns."""

from database.core.audits.base.base_pos_audit import BasePOSAudit
from database.core.storage.sqlite.database import SQLiteDatabase
from datetime import datetime, timedelta
from collections import Counter


class RefundSpikeAudit(BasePOSAudit):
    """
    Detects refund spikes compared to 30-day moving average.

    Flags HIGH risk if refunds spike > 280% of daily average.
    Flags MEDIUM risk if refunds spike > 150% of daily average.
    """

    code = "refund_spike"
    name = "Refund Spike Detection"

    def __init__(self):
        super().__init__()
        self._db = SQLiteDatabase()

    def analyze(self):
        """
        Analyze refund patterns and detect anomalies.

        Returns:
            dict: Refund statistics, spike ratios, and risk assessment.
        """
        today = datetime.now().strftime("%Y-%m-%d")

        # ─── Today's refunds ───
        today_orders = self.get_orders(
            domain=[
                ("state", "=", "done"),
                ("date_order", "like", f"{today}%"),
            ],
            fields=["id", "amount_total", "date_order", "user_id", "name"],
        )
        today_refunds = [o for o in today_orders if o.get("amount_total", 0) < 0]
        today_count = len(today_refunds)
        today_amount = abs(
            sum(o["amount_total"] for o in today_refunds)
        ) if today_refunds else 0.0

        # ─── 30-day moving average ───
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        rows = self._db.query(
            """
            SELECT 
                COUNT(*) as count,
                COALESCE(SUM(ABS(amount_total)), 0) as amount
            FROM pos_orders
            WHERE amount_total < 0 AND date_order >= ?
            """,
            (thirty_days_ago,),
        )

        hist_count = rows[0]["count"] if rows else 0
        hist_amount = rows[0]["amount"] if rows else 0

        daily_avg = hist_count / 30.0 if hist_count > 0 else 0.0
        daily_avg_amount = hist_amount / 30.0 if hist_amount > 0 else 0.0

        # ─── Spike ratios ───
        spike_ratio = (today_count / daily_avg) if daily_avg > 0 else 0.0
        amount_spike = (today_amount / daily_avg_amount) if daily_avg_amount > 0 else 0.0

        # ─── Risk assessment ───
        risk = "LOW"
        if spike_ratio > 2.8 or amount_spike > 2.8:
            risk = "HIGH"
        elif spike_ratio > 1.5 or amount_spike > 1.5:
            risk = "MEDIUM"

        # ─── Top cashiers by refund count ───
        cashiers = Counter(o.get("user_id", "Unknown") for o in today_refunds)
        top_cashiers = [
            {"cashier_id": c, "refund_count": n}
            for c, n in cashiers.most_common(5)
        ]

        # ─── Top refunds by amount ───
        top_refunds = sorted(
            today_refunds,
            key=lambda o: abs(o.get("amount_total", 0)),
            reverse=True,
        )[:5]
        top_refunds_summary = [
            {
                "order_id": o["id"],
                "order_name": o.get("name", ""),
                "amount": round(abs(o["amount_total"]), 2),
                "cashier_id": o.get("user_id"),
            }
            for o in top_refunds
        ]

        return {
            "today_refunds": today_count,
            "today_amount": round(today_amount, 2),
            "daily_avg_refunds": round(daily_avg, 2),
            "daily_avg_amount": round(daily_avg_amount, 2),
            "spike_ratio": round(spike_ratio, 2),
            "amount_spike": round(amount_spike, 2),
            "risk_level": risk,
            "top_cashiers": top_cashiers,
            "top_refunds": top_refunds_summary,
        }
