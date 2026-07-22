from database.core.audits.missing_receipts_audit import MissingReceiptsAudit
from database.core.audits.refunds.refund_audit import RefundAudit
from database.core.audits.pos_sales_summary_audit import POSSalesSummaryAudit
from database.core.audits.pos_daily_summary_audit import POSDailySummaryAudit
from database.core.audits.payment_method_summary_audit import PaymentMethodSummaryAudit


class AuditRegistry:

    def __init__(self):

        self._audits = {}

        self.register(MissingReceiptsAudit())
        self.register(RefundAudit())
        self.register(POSSalesSummaryAudit())
        self.register(POSDailySummaryAudit())
        self.register(PaymentMethodSummaryAudit())

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
