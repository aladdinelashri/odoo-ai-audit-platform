"""
Audit Registry - Registry Pattern for all audit modules.
Central registry to dynamically discover and run audits.
"""

import importlib
import logging
from typing import Dict, Callable, Any, Optional
from dataclasses import dataclass

from config.logging import get_logger

logger = get_logger("audit.registry")


@dataclass
class AuditInfo:
    """Metadata for a registered audit."""
    name: str
    code: str
    description: str
    module_path: str
    func_name: str = "run"
    category: str = "pos"


class AuditRegistry:
    """Central registry for all audit modules."""

    def __init__(self):
        self._audits: Dict[str, AuditInfo] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register all built-in audits."""
        defaults = [
            AuditInfo("missing_receipts", "MISSING_RCPT", "Detect missing receipts", "database.core.audits.missing_receipts_audit"),
            AuditInfo("refunds", "REFUNDS", "Analyze refund patterns", "database.core.audits.refunds.refund_spike_audit"),
            AuditInfo("daily_summary", "DAILY_SUM", "Daily POS summary", "database.core.audits.pos_daily_summary_audit"),
            AuditInfo("monthly_summary", "MONTHLY_SUM", "Monthly POS summary", "database.core.audits.pos_monthly_summary_audit"),
            AuditInfo("sales_summary", "SALES_SUM", "Sales performance summary", "database.core.audits.pos_sales_summary_audit"),
            AuditInfo("payment_methods", "PAY_METH", "Payment method breakdown", "database.core.audits.payment_method_summary_audit"),
            AuditInfo("cashier_performance", "CASH_PERF", "Cashier performance KPI", "database.core.audits.cashier_performance_audit"),
            AuditInfo("session", "SESSION", "POS session audit", "database.core.audits.session_audit"),
            AuditInfo("business_unit_kpi", "BU_KPI", "Business unit KPI", "database.core.audits.business_unit_kpi_audit"),
            AuditInfo("category_ranking", "CAT_RANK", "Category daily ranking", "database.core.audits.pos_category_daily_ranking_audit"),
        ]
        for audit in defaults:
            self.register(audit)

    def register(self, audit: AuditInfo) -> None:
        """Register an audit module."""
        self._audits[audit.name] = audit
        logger.debug(f"Registered audit: {audit.name} ({audit.code})")

    def get(self, name: str) -> Optional[AuditInfo]:
        """Get audit metadata by name."""
        return self._audits.get(name)

    def list_audits(self, category: str = None) -> Dict[str, AuditInfo]:
        """List all registered audits, optionally filtered by category."""
        if category:
            return {k: v for k, v in self._audits.items() if v.category == category}
        return self._audits.copy()

    def run(self, name: str, context, **kwargs) -> Any:
        """Dynamically load and run an audit by name."""
        audit = self.get(name)
        if not audit:
            raise ValueError(f"Audit '{name}' not found. Available: {list(self._audits.keys())}")
        try:
            module = importlib.import_module(audit.module_path)
            func = getattr(module, audit.func_name, None)
            if not func:
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if callable(attr) and not attr_name.startswith("_"):
                        func = attr
                        break
            if not func:
                raise AttributeError(f"No callable found in {audit.module_path}")
            logger.info(f"Running audit: {audit.name} ({audit.code})")
            return func(context, **kwargs)
        except Exception as e:
            logger.error(f"Failed to run audit '{name}': {e}")
            raise


registry = AuditRegistry()
