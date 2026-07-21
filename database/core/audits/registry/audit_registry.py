from database.core.audits.missing_receipts_audit import MissingReceiptsAudit
from database.core.audits.refunds.refund_audit import RefundAudit


class AuditRegistry:

    def __init__(self):

        self._audits = {}

        self.register(MissingReceiptsAudit())
        self.register(RefundAudit())

    def register(self, audit):

        self._audits[audit.code] = audit

    def get(self, code):

        return self._audits[code]

    def list(self):

        return list(self._audits.keys())

    def all(self):

        return list(self._audits.values())
