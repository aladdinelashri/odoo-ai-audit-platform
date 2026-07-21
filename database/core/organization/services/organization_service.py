from .business_unit_service import BusinessUnitService


class OrganizationService:

    def __init__(self):

        self.business_unit_service = BusinessUnitService()

    def resolve(self, order):

        return self.business_unit_service.resolve(order)
