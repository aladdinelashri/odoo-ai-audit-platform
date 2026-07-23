# database/core/audits/pos_category_daily_ranking_audit.py

from database.core.audits.base.base_pos_audit import BasePOSAudit
from database.core.storage.sqlite.database import SQLiteDatabase


class POSCategoryDailyRankingAudit(BasePOSAudit):

    code = "pos_category_daily_ranking"
    name = "POS Category Daily Ranking Audit"

    def __init__(self):
        super().__init__()
        self._db = SQLiteDatabase()

    def analyze(self):
        """
        Rank POS categories by daily sales.
        
        Returns:
            list[dict]: Daily ranking per category
        """

        rows = self._db.query("""
            SELECT 
                strftime('%Y-%m-%d', o.order_date) as day,
                pp.categ_id,
                pp.categ_name,
                COUNT(DISTINCT ol.order_id) as orders,
                SUM(ol.qty) as total_qty,
                SUM(ol.price_subtotal) as total_sales
            FROM pos_order_lines ol
            JOIN pos_orders o ON ol.order_id = o.id
            JOIN product_products pp ON ol.product_id = pp.id
            WHERE o.state = 'done'
            GROUP BY day, pp.categ_id
            ORDER BY day DESC, total_sales DESC
        """)

        result = []
        for row in rows:
            result.append({
                "date": row["day"],
                "category_id": row["categ_id"],
                "category_name": row["categ_name"],
                "orders": row["orders"],
                "total_qty": round(row["total_qty"] or 0, 2),
                "total_sales": round(row["total_sales"] or 0, 2),
                "average_order_value": round((row["total_sales"] or 0) / (row["orders"] or 1), 2),
            })

        return result
