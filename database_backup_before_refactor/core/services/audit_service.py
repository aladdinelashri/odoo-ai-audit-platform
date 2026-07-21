from database.core.services.pos_audit_service import POSAuditService
from database.core.services.accounting_audit_service import AccountingAuditService


class AuditService:
    """
    Main Audit Service.

    Entry point for all audit modules.
    """

    def __init__(self):
        self.pos = POSAuditService()
        self.accounting = AccountingAuditService()

    def system_summary(self):
        return {
            "pos": self.pos.summary(),
            "accounting": self.accounting.summary(),
        }

    def health_check(self):
        return {
            "latest_order": self.pos.latest_paid_order(),
            "latest_payment": self.pos.latest_payment(),
            "latest_session": self.pos.latest_session(),
            "latest_account_move": self.accounting.latest_posted_move(),
        }
