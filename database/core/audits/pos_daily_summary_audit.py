"""
POS Daily Summary Audit
Generates daily operational snapshots.
"""
from database.core.audits.base.base_pos_audit import BasePOSAudit
from database.core.storage.sqlite.sqlite_pool import SQLitePool
from datetime import datetime, timedelta


class POSDailySummaryAudit(BasePOSAudit):
    code = "daily_summary"
    name = "POS Daily Summary Audit"
    
    def analyze(self):
        """
        Generate daily summary for the last 7 days.
        
        Returns:
            Dict with audit results
        """
        findings = []
        query_time_ms = 0
        queries_executed = 0
        
        try:
            import time
            start = time.perf_counter()
            
            conn = SQLitePool.get_connection()
            cursor = conn.cursor()
            
            # Get daily summary
            cursor.execute("""
                SELECT 
                    DATE(date_order) as date,
                    COUNT(*) as order_count,
                    SUM(amount_total) as total_sales,
                    AVG(amount_total) as avg_order,
                    SUM(CASE WHEN amount_total < 0 THEN amount_total ELSE 0 END) as refunds,
                    COUNT(CASE WHEN amount_total < 0 THEN 1 END) as refund_count
                FROM pos_orders
                WHERE state = 'done'
                    AND date_order >= DATE('now', '-7 days')
                GROUP BY DATE(date_order)
                ORDER BY date DESC
            """)
            queries_executed += 1
            
            rows = cursor.fetchall()
            
            for row in rows:
                findings.append({
                    "type": "daily_summary",
                    "severity": "INFO",
                    "date": row['date'],
                    "order_count": row['order_count'],
                    "total_sales": row['total_sales'] or 0,
                    "avg_order": round(row['avg_order'] or 0, 2),
                    "refunds": row['refunds'] or 0,
                    "refund_count": row['refund_count'] or 0
                })
            
            end = time.perf_counter()
            query_time_ms = (end - start) * 1000
            
            return {
                "audit_code": self.code,
                "name": self.name,
                "category": self.category,
                "status": "PASS" if findings else "WARNING",
                "findings": findings,
                "findings_count": len(findings),
                "performance": {
                    "query_time_ms": round(query_time_ms, 2),
                    "queries_executed": queries_executed
                }
            }
            
        except Exception as e:
            return {
                "audit_code": self.code,
                "name": self.name,
                "category": self.category,
                "status": "ERROR",
                "error": str(e),
                "findings": [],
                "findings_count": 0
            }
