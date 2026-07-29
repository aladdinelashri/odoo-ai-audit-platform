"""
Refund Spike Audit
Detects unusual spikes in refund activity.
"""
from database.core.audits.base.base_pos_audit import BasePOSAudit
from database.core.storage.sqlite.sqlite_pool import SQLitePool
from datetime import datetime, timedelta


class RefundSpikeAudit(BasePOSAudit):
    code = "refunds"
    name = "Refund Spike Audit"
    
    def analyze(self):
        """
        Detect refund spikes using 30-day moving average.
        
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
            
            # Get daily refund counts for the last 30 days
            cursor.execute("""
                SELECT 
                    DATE(date_order) as date,
                    COUNT(*) as refund_count,
                    SUM(amount_total) as refund_amount
                FROM pos_orders
                WHERE state = 'done' 
                    AND amount_total < 0
                    AND date_order >= DATE('now', '-30 days')
                GROUP BY DATE(date_order)
                ORDER BY date
            """)
            queries_executed += 1
            
            daily_refunds = cursor.fetchall()
            
            if len(daily_refunds) >= 7:  # Need at least 7 days for meaningful analysis
                # Calculate moving average
                for i in range(len(daily_refunds)):
                    day = daily_refunds[i]
                    # Use 7-day moving average
                    start_idx = max(0, i - 6)
                    window = daily_refunds[start_idx:i]
                    
                    if window:
                        avg_count = sum(r['refund_count'] for r in window) / len(window)
                        avg_amount = sum(r['refund_amount'] for r in window) / len(window)
                        
                        current_count = day['refund_count']
                        current_amount = day['refund_amount'] or 0
                        
                        # Check if current day is significantly above average (2x or more)
                        if avg_count > 0 and current_count > avg_count * 2:
                            findings.append({
                                "type": "refund_spike_count",
                                "severity": "HIGH" if current_count > avg_count * 3 else "MEDIUM",
                                "message": f"Refund spike detected on {day['date']}",
                                "date": day['date'],
                                "refund_count": current_count,
                                "avg_count": round(avg_count, 1),
                                "refund_amount": current_amount,
                                "avg_amount": round(avg_amount, 2)
                            })
            
            end = time.perf_counter()
            query_time_ms = (end - start) * 1000
            
            status = "FAIL" if findings else "PASS"
            
            return {
                "audit_code": self.code,
                "name": self.name,
                "category": self.category,
                "status": status,
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
