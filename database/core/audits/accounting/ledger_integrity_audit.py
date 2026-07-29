"""
Ledger Integrity Audit - Checks for negative asset balances, orphaned accounts, zero-balance AR/AP.
"""
import sqlite3
import logging
from typing import List, Optional, Dict, Any

from database.core.audits.base.base_audit import BaseAudit
from database.core.storage.sqlite.sqlite_pool import SQLitePool

logger = logging.getLogger(__name__)


class LedgerFinding:
    def __init__(self, issue_type: str, severity: str, message: str,
                 account_id: Optional[int] = None, **kwargs):
        self.issue_type = issue_type
        self.severity = severity
        self.message = message
        self.account_id = account_id
        self.extra = kwargs

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "type": self.issue_type,
            "severity": self.severity,
            "message": self.message,
        }
        if self.account_id:
            result["account_id"] = self.account_id
        result.update(self.extra)
        return result


class LedgerIntegrityAudit(BaseAudit):
    code = "ledger_integrity"
    name = "Ledger Integrity Audit"
    category = "accounting"

    def __init__(self, context: Optional[Dict] = None):
        super().__init__()
        self.context = context or {}
        self.findings: List[LedgerFinding] = []
        self.query_time_ms = 0
        self.queries_executed = 0

    def _safe_float(self, value) -> float:
        if value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def _safe_int(self, value) -> Optional[int]:
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    def analyze(self) -> Dict[str, Any]:
        import time
        start = time.perf_counter()
        self.findings = []
        self.queries_executed = 0

        try:
            conn = SQLitePool.get_connection()
            cursor = conn.cursor()

            # Check negative asset balances (asset accounts with negative total balance)
            cursor.execute("""
                SELECT 
                    aa.id,
                    aa.code,
                    aa.name,
                    aa.account_type,
                    COALESCE(SUM(aml.balance), 0) as total_balance
                FROM account_accounts aa
                LEFT JOIN account_move_lines aml ON aml.account_id = aa.id
                WHERE aa.account_type LIKE 'asset%'
                GROUP BY aa.id
                HAVING total_balance < -0.01
            """)
            self.queries_executed += 1
            neg_assets = cursor.fetchall()
            for row in neg_assets:
                self.findings.append(LedgerFinding(
                    issue_type="negative_asset_balance",
                    severity="HIGH",
                    message=f"Negative balance in asset account {row['code']}: {row['total_balance']:.2f}",
                    account_id=row["id"],
                    account_code=row["code"],
                    account_name=row["name"],
                    balance=self._safe_float(row["total_balance"])
                ))

            # Check zero-balance AR/AP
            cursor.execute("""
                SELECT 
                    aa.id,
                    aa.code,
                    aa.name,
                    aa.account_type,
                    COALESCE(SUM(aml.balance), 0) as total_balance
                FROM account_accounts aa
                LEFT JOIN account_move_lines aml ON aml.account_id = aa.id
                WHERE aa.account_type IN ('receivable', 'payable')
                GROUP BY aa.id
                HAVING ABS(total_balance) < 0.01
            """)
            self.queries_executed += 1
            zero_ar_ap = cursor.fetchall()
            for row in zero_ar_ap:
                self.findings.append(LedgerFinding(
                    issue_type="zero_balance_ar_ap",
                    severity="MEDIUM",
                    message=f"Zero balance in {row['account_type']} account {row['code']}",
                    account_id=row["id"],
                    account_code=row["code"],
                    account_name=row["name"],
                    balance=0.0
                ))

            # Check orphaned accounts (accounts with no moves)
            cursor.execute("""
                SELECT 
                    aa.id,
                    aa.code,
                    aa.name,
                    aa.account_type
                FROM account_accounts aa
                WHERE NOT EXISTS (
                    SELECT 1 FROM account_move_lines aml
                    WHERE aml.account_id = aa.id
                )
                AND aa.account_type NOT IN ('view', 'consolidation')
            """)
            self.queries_executed += 1
            orphans = cursor.fetchall()
            for row in orphans:
                self.findings.append(LedgerFinding(
                    issue_type="orphaned_account",
                    severity="LOW",
                    message=f"Orphaned account: {row['code']} ({row['name']}) - no moves",
                    account_id=row["id"],
                    account_code=row["code"],
                    account_name=row["name"]
                ))

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
            logger.error(f"Ledger integrity audit failed: {e}")
            return {
                "audit_code": self.code,
                "name": self.name,
                "category": self.category,
                "status": "ERROR",
                "error": str(e),
                "findings": [],
                "findings_count": 0
            }

    def run(self) -> Dict[str, Any]:
        return self.analyze()
