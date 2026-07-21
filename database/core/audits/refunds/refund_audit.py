from database.core.audits.base.base_audit import BaseAudit
from database.core.organization.services import OrganizationService
from database.core.repositories.pos_order_repository import POSOrderRepository


class RefundAudit(BaseAudit):

    code = "refunds"

    name = "POS Refund Audit"

    def __init__(self):

        self.repo = POSOrderRepository()
        self.organization_service = OrganizationService()

    def analyze(self):

        refunds = self.repo.search(
            [
                ("amount_total", "<", 0),
            ],
            fields=[
                "id",
                "name",
                "date_order",
                "amount_total",
                "session_id",
                "company_id",
            ],
        )

        result = []

        for refund in refunds:

            business_unit = self.organization_service.resolve(refund)

            result.append(
                {
                    "refund_id": refund["id"],
                    "receipt": refund["name"],
                    "amount": refund["amount_total"],
                    "business_unit": (
                        business_unit.name if business_unit else None
                    ),
                }
            )

        return result
