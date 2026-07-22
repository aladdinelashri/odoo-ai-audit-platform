from database.core.organization.services.organization_service import (
    OrganizationService,
)
from database.core.context.audit_context import AuditContext


class AuditContextBuilder:

    def __init__(self):

        self.organization_service = OrganizationService()

    def build(self, order):

        company = order.get("company_id")

        company_id = (
            company
            if isinstance(company, int)
            else (company[0] if company else None)
        )

        return AuditContext(
            company_id=company_id,
            business_unit=self.organization_service.resolve(order),
            profile=None,
        )
