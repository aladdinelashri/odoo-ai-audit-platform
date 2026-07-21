from database.core.profile import ProfileLoader
from database.core.organization.services import OrganizationService

from .audit_context import AuditContext


class AuditContextBuilder:

    def __init__(self):

        self.profile = ProfileLoader().load()
        self.organization_service = OrganizationService()

    def build(self, order):

        return AuditContext(
            profile=self.profile,
            business_unit=self.organization_service.resolve(order),
            company_id=order["company_id"][0]
            if order.get("company_id")
            else None,
            session_id=order["session_id"][0]
            if order.get("session_id")
            else None,
            metadata={},
        )
