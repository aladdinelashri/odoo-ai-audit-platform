from dataclasses import dataclass

from database.core.profile import ClientProfile
from database.core.organization.entity import BusinessUnit


@dataclass
class AuditContext:

    profile: ClientProfile

    business_unit: BusinessUnit | None = None

    company_id: int | None = None

    session_id: int | None = None

    metadata: dict | None = None
