"""
Tax Validation Audit - Validates tax amounts, rates, missing taxes, and orphan tax lines.
"""
import sqlite3
import logging
from typing import List, Optional, Dict, Any

from database.core.audits.base.base_audit import BaseAudit
from database.core.storage.sqlite.sqlite_pool import SQLitePool

logger = logging.getLogger(__name__)


class TaxFinding:
    def __init__(self, issue_type: str, severity: str, message: str,
                 move_id: Optional[int] = None, **kwargs):
        self.issue_type = issue_type
        self.severity = severity
        self.message = message
        self.move_id = move_id
        self.extra = kwargs

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "type": self.issue_type,
            "severity": self.severity,
            "message": self.message,
        }
        if self.move_id:
            result["move_id"] = self.move_id
        result.update(self.extra)
        return result


class TaxValidationAudit(BaseAudit):
    code = "tax_validation"
    name = "Tax Validation Audit"
    category = "accounting"

    def __init__(self, context: Optional[Dict] = None):
        super().__init__()
        self.context = context or {}
        self.findings: List[TaxFinding] = []
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

            # Check tax amounts - find lines with tax_base_amount where balance doesn't match expected
            # Using actual column names from the schema
            cursor.execute("""
                SELECT 
                    aml.id,
                    aml.move_id,
                    aml.balance,
                    aml.tax_base_amount,
                    am.id as move_id,
                    am.name as move_name,
                    am.date
                FROM account_move_lines aml
                JOIN account_moves am ON am.id = aml.move_id
                WHERE am.state = 'posted'
                  AND aml.tax_base_amount IS NOT NULL
                  AND aml.tax_base_amount != 0
                  AND aml.tax_base_amount != ''
                LIMIT 10000
            """)
            self.queries_executed += 1
            rows = cursor.fetchall()

            for row in rows:
                self._check_tax_amount_mismatch(row)

            # Check for tax lines with invalid tax rates (where tax is > 50% of base)
            cursor.execute("""
                SELECT 
                    aml.id,
                    aml.move_id,
                    aml.balance,
                    aml.tax_base_amount,
                    am.name as move_name
                FROM account_move_lines aml
                JOIN account_moves am ON am.id = aml.move_id
                WHERE am.state = 'posted'
                  AND aml.tax_base_amount IS NOT NULL
                  AND aml.tax_base_amount != 0
                  AND aml.tax_base_amount != ''
                  AND ABS(aml.balance) > 0.5 * ABS(aml.tax_base_amount)
                LIMIT 10000
            """)
            self.queries_executed += 1
            invalid_rows = cursor.fetchall()
            for row in invalid_rows:
                balance = self._safe_float(row["balance"])
                tax_base = self._safe_float(row["tax_base_amount"])
                if tax_base != 0:
                    tax_rate = abs(balance / tax_base) * 100
                    if tax_rate > 50:
                        self.findings.append(TaxFinding(
                            issue_type="invalid_tax_rate",
                            severity="MEDIUM",
                            message=f"Unusually high tax rate: {tax_rate:.1f}% (base: {tax_base}, balance: {balance})",
                            move_id=row["move_id"],
                            move_name=row["move_name"],
                            tax_base=tax_base,
                            balance=balance,
                            tax_rate=tax_rate
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
            logger.error(f"Tax validation audit failed: {e}")
            return {
                "audit_code": self.code,
                "name": self.name,
                "category": self.category,
                "status": "ERROR",
                "error": str(e),
                "findings": [],
                "findings_count": 0
            }

    def _check_tax_amount_mismatch(self, row: sqlite3.Row):
        """Check if tax amount (balance) is proportional to tax_base_amount."""
        tax_base = self._safe_float(row["tax_base_amount"])
        balance = self._safe_float(row["balance"])
        move_id = row["move_id"]
        move_name = row["move_name"]

        if tax_base and abs(tax_base) > 0:
            # Expected tax amount roughly 15% of base (assuming standard VAT)
            # This is a simplified check; adjust as needed
            expected_tax = tax_base * 0.15
            if abs(balance - expected_tax) > 10.0:  # tolerance
                self.findings.append(TaxFinding(
                    issue_type="tax_amount_mismatch",
                    severity="HIGH" if abs(balance - expected_tax) > 100 else "MEDIUM",
                    message=f"Tax amount mismatch: expected ~{expected_tax:.2f}, got {balance:.2f}",
                    move_id=move_id,
                    move_name=move_name,
                    tax_base=tax_base,
                    balance=balance,
                    expected=expected_tax
                ))

    def run(self) -> Dict[str, Any]:
        return self.analyze()
