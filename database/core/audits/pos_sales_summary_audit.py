"""
POS Sales Summary Audit
Aggregates branch-level sales performance.
"""
from database.core.audits.base.base_pos_audit import BasePOSAudit
from database.core.storage.sqlite.sqlite_pool import SQLitePool


class POSSalesSummaryAudit(BasePOSAudit):
    code = "sales_summary"
    name = "POS Sales Summary Audit"
    
    def analyze(self):
        """
        Generate sales summary by branch/business unit.
        
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
            
            # Get sales summary by business unit
            cursor.execute("""
                SELECT 
                    COALESCE(bu.name, 'Unknown') as business_unit,
                    COUNT(*) as order_count,
                    SUM(amount_total) as total_sales,
                    AVG(amount_total) as avg_order_value,
                    MIN(amount_total) as min_order,
                    MAX(amount_total) as max_order,
                    SUM(CASE WHEN amount_total < 0 THEN amount_total ELSE 0 END) as refunds
                FROM pos_orders po
                LEFT JOIN session_business_units sbu ON sbu.session_id = po.session_id
                LEFT JOIN business_units bu ON bu.id = sbu.business_unit_id
                WHERE po.state = 'done'
                GROUP BY bu.id
                ORDER BY total_sales DESC
            """)
            queries_executed += 1
            
            rows = cursor.fetchall()
            
            for row in rows:
                findings.append({
                    "type": "sales_summary",
                    "severity": "INFO",
                    "business_unit": row['business_unit'],
                    "order_count": row['order_count'],
                    "total_sales": row['total_sales'] or 0,
                    "avg_order_value": round(row['avg_order_value'] or 0, 2),
                    "min_order": row['min_order'] or 0,
                    "max_order": row['max_order'] or 0,
                    "refunds": row['refunds'] or 0
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
