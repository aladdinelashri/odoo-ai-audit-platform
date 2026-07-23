# database/core/audits/registry/audit_registry.py

from database.core.audits.missing_receipts_audit import MissingReceiptsAudit
from database.core.audits.refunds.refund_audit import RefundAudit
from database.core.audits.pos_sales_summary_audit import POSSalesSummaryAudit
from database.core.audits.pos_daily_summary_audit import POSDailySummaryAudit
from database.core.audits.payment_method_summary_audit import PaymentMethodSummaryAudit
from database.core.audits.pos_monthly_summary_audit import POSMonthlySummaryAudit
from database.core.audits.cashier_performance_audit import CashierPerformanceAudit
from database.core.audits.session_audit import SessionAudit
from database.core.audits.business_unit_kpi_audit import BusinessUnitKPIAudit
from database.core.audits.pos_category_daily_ranking_audit import POSCategoryDailyRankingAudit


class AuditRegistry:

    def __init__(self):

        self._audits = {}

        self.register(MissingReceiptsAudit())
        self.register(RefundAudit())
        self.register(POSSalesSummaryAudit())
        self.register(POSDailySummaryAudit())
        self.register(PaymentMethodSummaryAudit())
        self.register(POSMonthlySummaryAudit())
        self.register(CashierPerformanceAudit())
        self.register(SessionAudit())
        self.register(BusinessUnitKPIAudit())
        self.register(POSCategoryDailyRankingAudit())

    def register(self, audit):

        self._audits[audit.code] = audit

    def get(self, code):

        return self._audits[code]

    def create(self, code):

        return self.get(code)

    def list(self):

        return list(self._audits.keys())

    def all(self):

        return list(self._audits.values())
