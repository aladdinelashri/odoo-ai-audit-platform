"""
Journal Audit - Checks for unbalanced entries, sequence gaps, duplicates, missing partners, and future-dated postings.
"""
import sqlite3
import logging
import re
from typing import List, Optional, Dict, Any
from datetime import datetime

from database.core.audits.base.base_audit import BaseAudit
from database.core.storage.sqlite.sqlite_pool import SQLitePool

logger = logging.getLogger(__name__)


class JournalFinding:
    """Represents a single finding from the journal audit."""
    
    def __init__(self, issue_type: str, severity: str, message: str, 
                 move_id: Optional[int] = None, **kwargs):
        self.issue_type = issue_type
        self.severity = severity
        self.message = message
        self.move_id = move_id
        self.extra = kwargs
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "type": self.issue_type,
            "severity": self.severity,
            "message": self.message,
        }
        if self.move_id:
            result["move_id"] = self.move_id
        result.update(self.extra)
        return result


class JournalAudit(BaseAudit):
    """Audit for journal entries."""
    
    code = "journal_audit"
    name = "Journal Audit"
    category = "accounting"
    
    def __init__(self, context: Optional[Dict] = None):
        super().__init__()  # No arguments – BaseAudit.__init__ takes only self
        self.context = context or {}
        self.findings: List[JournalFinding] = []
        self.query_time_ms = 0
        self.queries_executed = 0
    
    def _safe_float(self, value) -> float:
        """Safely convert a value to float."""
        if value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def _safe_int(self, value) -> Optional[int]:
        """Safely convert a value to int."""
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    
    def _extract_id(self, value) -> Optional[int]:
        """Extract ID from a many2one field (could be int or tuple)."""
        if isinstance(value, int):
            return value
        if isinstance(value, (list, tuple)) and len(value) > 0:
            return self._safe_int(value[0])
        return self._safe_int(value)
    
    def analyze(self) -> Dict[str, Any]:
        """Run the journal audit using a CTE single-query pattern."""
        import time
        start = time.perf_counter()
        self.findings = []
        self.queries_executed = 0
        
        try:
            conn = SQLitePool.get_connection()
            cursor = conn.cursor()
            
            # CTE single-query for all checks
            query = """
            WITH move_balances AS (
                SELECT 
                    move_id,
                    SUM(COALESCE(debit, 0)) as total_debit,
                    SUM(COALESCE(credit, 0)) as total_credit,
                    COUNT(*) as line_count,
                    SUM(CASE WHEN account_id IS NULL THEN 1 ELSE 0 END) as null_accounts
                FROM account_move_lines
                GROUP BY move_id
            ),
            duplicate_names AS (
                SELECT name, COUNT(*) as cnt
                FROM account_moves
                WHERE state = 'posted' AND name IS NOT NULL
                GROUP BY name
                HAVING COUNT(*) > 1
            )
            SELECT 
                am.id,
                am.name,
                am.state,
                am.date,
                am.journal_id,
                am.partner_id,
                am.amount_total,
                am.create_date,
                COALESCE(mb.total_debit, 0) as total_debit,
                COALESCE(mb.total_credit, 0) as total_credit,
                COALESCE(mb.line_count, 0) as line_count,
                COALESCE(mb.null_accounts, 0) as null_accounts,
                dn.cnt as duplicate_count
            FROM account_moves am
            LEFT JOIN move_balances mb ON mb.move_id = am.id
            LEFT JOIN duplicate_names dn ON dn.name = am.name
            WHERE am.state = 'posted'
            ORDER BY am.date DESC, am.id DESC
            """
            
            cursor.execute(query)
            self.queries_executed += 1
            rows = cursor.fetchall()
            
            for row in rows:
                # Check each condition
                self._check_unbalanced_entries(row)
                self._check_duplicate_entries(row)
                self._check_missing_partner(row)
                self._check_future_dated_postings(row)
            
            # Process sequence gaps separately (requires a second query)
            self._process_sequence_gaps()
            
            end = time.perf_counter()
            self.query_time_ms = (end - start) * 1000
            
            findings_list = [f.to_dict() for f in self.findings]
            
            status = "FAIL" if findings_list else "PASS"
            
            return {
                "audit_code": self.code,
                "name": self.name,
                "category": self.category,
                "status": status,
                "findings": findings_list,
                "findings_count": len(findings_list),
                "performance": {
                    "query_time_ms": round(self.query_time_ms, 2),
                    "queries_executed": self.queries_executed
                }
            }
            
        except Exception as e:
            logger.error(f"Journal audit failed: {e}")
            return {
                "audit_code": self.code,
                "name": self.name,
                "category": self.category,
                "status": "ERROR",
                "error": str(e),
                "findings": [],
                "findings_count": 0
            }
    
    def _check_unbalanced_entries(self, row: sqlite3.Row) -> None:
        """Check if an entry is unbalanced (total_debit != total_credit)."""
        total_debit = self._safe_float(row["total_debit"])
        total_credit = self._safe_float(row["total_credit"])
        
        if abs(total_debit - total_credit) > 0.001:  # floating point tolerance
            self.findings.append(JournalFinding(
                issue_type="unbalanced_entry",
                severity="HIGH",
                message=f"Unbalanced entry: debit={total_debit}, credit={total_credit}",
                move_id=row["id"],
                move_name=row["name"],
                total_debit=total_debit,
                total_credit=total_credit,
                difference=total_debit - total_credit
            ))
    
    def _check_duplicate_entries(self, row: sqlite3.Row) -> None:
        """Check for duplicate entries based on duplicate_count from CTE."""
        dup_count = self._safe_int(row["duplicate_count"])
        if dup_count and dup_count > 1:
            self.findings.append(JournalFinding(
                issue_type="duplicate_entry",
                severity="MEDIUM",
                message=f"Duplicate entry name '{row['name']}' appears {dup_count} times",
                move_id=row["id"],
                move_name=row["name"],
                duplicate_count=dup_count
            ))
    
    def _check_missing_partner(self, row: sqlite3.Row) -> None:
        """Check if a posted entry has no partner but amount > 0."""
        partner_id = self._extract_id(row["partner_id"])
        if partner_id is not None:
            return
        
        amount = self._safe_float(row["amount_total"])
        if amount > 0:
            self.findings.append(JournalFinding(
                issue_type="missing_partner",
                severity="MEDIUM",
                message=f"Missing partner for transaction with amount {amount}",
                move_id=row["id"],
                move_name=row["name"],
                amount_total=amount
            ))
    
    def _check_future_dated_postings(self, row: sqlite3.Row) -> None:
        """Check if a posting has a future date (compared to today)."""
        date_str = row["date"]
        if not date_str:
            return
        
        try:
            # Assume date is in ISO format (YYYY-MM-DD)
            posting_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            today = datetime.now().date()
            if posting_date > today:
                self.findings.append(JournalFinding(
                    issue_type="future_dated_posting",
                    severity="LOW",
                    message=f"Future-dated posting on {posting_date}",
                    move_id=row["id"],
                    move_name=row["name"],
                    date=date_str
                ))
        except ValueError:
            # If date format is different, skip
            pass
    
    def _process_sequence_gaps(self) -> None:
        """
        Separate method to detect sequence gaps across all entries.
        This runs after the main query to avoid N+1.
        """
        try:
            conn = SQLitePool.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT journal_id, name, id
                FROM account_moves
                WHERE state = 'posted'
                ORDER BY journal_id, name
            """)
            self.queries_executed += 1
            rows = cursor.fetchall()
            
            # Group by journal_id
            journals = {}
            for row in rows:
                jid = row["journal_id"]
                if jid not in journals:
                    journals[jid] = []
                journals[jid].append((row["name"], row["id"]))
            
            for jid, entries in journals.items():
                # Extract numeric part from name
                numbers = []
                for name, mid in entries:
                    if name:
                        match = re.search(r'(\d+)', name)
                        if match:
                            numbers.append((int(match.group(1)), mid, name))
                numbers.sort()
                
                # Check gaps
                for i in range(len(numbers) - 1):
                    cur_num, cur_id, cur_name = numbers[i]
                    next_num, next_id, next_name = numbers[i+1]
                    if next_num - cur_num > 1:
                        self.findings.append(JournalFinding(
                            issue_type="sequence_gap",
                            severity="MEDIUM",
                            message=f"Sequence gap between {cur_name} and {next_name}",
                            move_id=cur_id,
                            journal_id=jid,
                            gap_start=cur_num,
                            gap_end=next_num,
                            missing_count=next_num - cur_num - 1
                        ))
        except Exception as e:
            logger.warning(f"Error checking sequence gaps: {e}")
    
    def run(self) -> Dict[str, Any]:
        """Alias for analyze() to match BaseAudit interface."""
        return self.analyze()
