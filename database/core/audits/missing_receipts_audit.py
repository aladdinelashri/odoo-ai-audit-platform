"""
Missing Receipts Audit
Detects sequential gaps in receipt numbering.
"""
from database.core.audits.base.base_pos_audit import BasePOSAudit
from database.core.storage.sqlite.sqlite_pool import SQLitePool


class MissingReceiptsAudit(BasePOSAudit):
    code = "missing_receipts"
    name = "Missing Receipts Audit"
    
    def analyze(self):
        """
        Detect gaps in receipt numbering.
        
        Returns:
            Dict with audit results
        """
        findings = []
        query_time_ms = 0
        queries_executed = 0
        
        try:
            import time
            start = time.perf_counter()
            
            # Get all receipt numbers sorted
            conn = SQLitePool.get_connection()
            cursor = conn.cursor()
            
            # Get all receipt numbers for completed orders
            cursor.execute("""
                SELECT id, receipt_number, session_id, date_order 
                FROM pos_orders 
                WHERE state = 'done' AND receipt_number IS NOT NULL
                ORDER BY receipt_number
            """)
            queries_executed += 1
            
            rows = cursor.fetchall()
            if rows and len(rows) > 1:
                # Check for gaps
                for i in range(len(rows) - 1):
                    current = rows[i]
                    next_row = rows[i + 1]
                    
                    # Try to extract numeric part of receipt number
                    current_num = self._extract_number(current['receipt_number'])
                    next_num = self._extract_number(next_row['receipt_number'])
                    
                    if current_num and next_num and next_num - current_num > 1:
                        findings.append({
                            "type": "receipt_gap",
                            "severity": "MEDIUM",
                            "message": f"Gap in receipt numbering: {current_num} -> {next_num}",
                            "current_receipt": current['receipt_number'],
                            "next_receipt": next_row['receipt_number'],
                            "current_id": current['id'],
                            "next_id": next_row['id'],
                            "date": current['date_order']
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
    
    def _extract_number(self, receipt_number):
        """Extract numeric part from receipt number."""
        if not receipt_number:
            return None
        import re
        match = re.search(r'(\d+)', str(receipt_number))
        if match:
            return int(match.group(1))
        return None
